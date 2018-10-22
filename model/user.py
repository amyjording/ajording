import os, os.path
import cherrypy,json
import datetime
import pymongo
from cherrypy import request
from itsdangerous import URLSafeTimedSerializer

#later project - mongo schema validation could reduce several lines of code
#https://stackoverflow.com/questions/46569262/does-pymongo-have-validation-rules-built-in
class User(object):

    #reference this!! -- https://codereview.stackexchange.com/questions/161340/models-in-a-simple-pymongo-based-blogging-web-app-without-orm-odm
    # no date needed if default id: https://stackoverflow.com/questions/3778428/best-way-to-store-date-time-in-mongodb
    
    def __init__(self, _id=None, username=None, email=None, password=None, 
                name=None, activated=False, session_id=u'', last_login=None,
                ip=u'', following=[], followers=[], deleted=False ):
        from db.mongo import get_db
        user_db = get_db(collection_name=secrets.collection2)
        
        self._id = _id #gets generated upon saving to collection
        self.username = username #generated on instance, passed in via param
        self.email = email #generated on instance, passed in via param
        self.password = password #generated on instance, passed in via param
        self.name = name #generated on instance, passed in via param
        self.activated = activated #generated when saved to collection, default False until activation token verifies and updated to True
        self.session_id = session_id #generated via session generator method, saves to database (session should begin at registration/saved)
        self.last_login = last_login
        self.ip = ip #captured in a method via cherrypy.request.headers, then stored in collection either at login or register
        self.following = following #generated as an empty list in collection at time of new save/register
        self.followers = followers #generated as an empty list in collection at time of new save/register
        self.deleted = deleted #generated at time of save/register with default set to False

## -- User Model functions for Controller to use -- ##

    @classmethod
    def new(cls, username, email, password, name):
        ip = cherrypy.request.headers.get("X-Forwarded-For",'0.0.0.0')
        return cls(username=username, email=email, password=password, name=name, ip=ip)

    @classmethod
    def get(cls, kw):
        if kw.get('_id'):
            this_user = user_db.find_one({'_id': kw['_id']})
        elif kw.get('email'):
            this_user = user_db.find_one({'email': kw['email']})
        elif kw.get('username'):
            this_user = user_db.find_one({'email': kw['username']})
        else:
            this_user = False
        return cls(_id=this_user['_id'], username=this_user['username'], email=this_user['email'], 
                    password=this_user['password'], name=this_user['name'], activated=this_user['activated'], 
                    session_id=this_user['session_id'], ip=this_user['ip'], following=this_user['following'], 
                    followers=this_user['followers'], deleted=this_user['deleted'])

    def update(self, dictonary_of_records_to_update):
        try:
            update_status = user_db.update_one({'_id': self._id}, {'$set': dictonary_of_records_to_update})
            if update_status.matched_count > 0:
                return True
        except pymongo.errors.PyMongoError as e:
            return False

## -- Before Saving New User, verify these inputs -- ##

    def check_unique_credentials(self):
        existing_email = user_db.find_one({'email': self.email})
        existing_username = user_db.find_one({'username': self.username})
        return existing_email, existing_username

    def check_length(text, max=60): 
        text = text[:max] 
        return text

    def valid_email(self):
        import re
        check_email = re.match(r'\A[\w+\-.]+@[a-z\d\-]+(\.[a-z\d\-]+)*\.[a-z]+', self.email, flags=0)

        if check_email:
            check_email_length = check_length(check_email, max=255)
            if check_email_length == self.email:
                return True
            else:
                return False
        else:
            return False

    def valid_username(self):
        import re
        check_username = re.match(r'\A.[0-9a-zA-Z_]+(\'.)*', self.username, flags=0)

        if check_username:
            check_username_length = check_length(check_username, max=60)
            if check_username_length == self.username:
                return True
            else:
                return False
        else:
            return False

    def valid_password(self):
        import re
        password = self.password
        if len(password) < 8:
            return "Password must be at least 8 characters."

        has_upper_case = re.search(r'[A-Z]+', password, flags=0)
        has_lower_case = re.search(r'[a-z]+', password, flags=0)
        has_numbers = re.search(r'\w[0-9]', password, flags=0)
        has_non_alphas = re.search(r'\W', password, flags=0)

        if len(has_upper_case.group(0)) and len(has_lower_case.group(0)) and len(has_numbers.group(0)) and len(has_non_alphas.group(0)) < 4:
            return False
        else:
            return True

    def encrypt_password(self):
        import bcrypt
        from string import ascii_letters
        from string import digits
        from string import ascii_lowercase
        password = self.password
        password = legal_string(password,128)
        hashpass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hashpass

    def verify_correct_password(password, hashpass):
        if (hashpass, password.encode('utf-8')) == password.encode('utf-8'):
            return True
        return False

    def before_save(self):
        if not self.username:
            return {'result_ok': False, 'error_msg':'Username cannot be blank.'}

        if not self.password:
            return {'result_ok': False, 'error_msg':'Password cannot be blank.'}

        if not self.email: # bare minimum
            return {'result_ok': False, 'error_msg':'Email cannot be blank.'}
        
        existing_email, existing_username = self.check_unique_credentials()

        if existing_email:
            return {'result_ok': False, 'error_msg': 'This email already has an account, please Sign in.'}
        elif existing_user:
            return {'result_ok': False, 'error_msg': 'This username has already been taken. Please choose another username.'}

        if self.valid_email() is False:
            return {'result_ok': False, 'error_msg':'Please enter a valid email.'}

        if self.valid_username() is False:
            return {'result_ok': False, 'error_msg':'Please enter a valid username.'}
        
        if self.valid_password() is False:
            return {'result_ok': False, 'error_msg':'Invalid Password. Please choose at least one uppercase letter, one lowercase letter, a number, and a symbol.'}
        else:
            return True    

## SAVE NEW USER
    def save(self):
        if user.before_save(): 
        
            hashpass = encrypt_password(self.password)    
            
            if check_length(self.name, max=255):
                name = self.name
            else:
                name = 'Portfolio Tourist'

            imported_user_data = {
                    u'_id': ObjectId(),
                    u'email': self.email,
                    u'username': self.username,
                    u'password': hashpass,
                    u'name': name,
                    u'activated': False,
                    u'session_id': u'',
                    u'ip': '',
                    u'following':[],
                    u'followers':[],
                    u'deleted': False
                    }

            add_new_user = user_db.insert_one(imported_user_data)
            
            return {'result_ok': True, 'email': email, 'name': username, 'fullname': name}
        else:
            return {'result_ok': False, 'error_msg': 'Unable to save user.'}

## ------------ END CREATE USER -------------##


## ---------- User Login, Session and Logout -------- ##

    def set_cookie(self):
        _id = self.id
        expiration = datetime.datetime.now() + datetime.timedelta(days=90)
        session_token = base64.urlsafe_b64encode(os.urandom(16))
        update_user_session = update_one_user(_id, {'session_id': session_token})  
        #cherrypy.incoming_hook({'text': "{0} for {1}".format(session_token, repr(user_id))})
        set_cookies = cherrypy.response.cookie
        set_cookies['session_token'] = session_token
        set_cookies['session_token']['path'] = "/"
        set_cookies['session_token']['domain'] = "amyjording.com"
        set_cookies['session_token']['expires'] = \
            expiration.strftime("%a, %d-%b-%Y %H:%M:%S UTC")    

    def authenticated():
        cookie = cherrypy.request.cookie
        check_for_token = cookie.get('session_token', None)
        if check_for_token != None:
            session_token = cookie['session_token'].value
            # fc_session_id = bcrypt.hashpw(session_token.encode('utf-8'), bcrypt.gensalt()) # session_token 
            uid_by_session = user.find_one({'session_id': session_token})
            if uid_by_session != None: # bcrypt.hashpw(session_token.encode('utf-8'), kw['fc_session_id'].encode('utf-8')) == kw['fc_session_id'].encode('utf-8'):
                return True
        return False

    def remember_user(self):
        this_ip = cherrypy.request.headers.get("X-Forwarded-For",'0.0.0.0')
        update_user_session_data = self.update({'last_login': datetime.datetime.utcnow(),'ip': this_ip})
        session_from_db = self.session_id
        cookie = cherrypy.response.cookie
        #cherrypy.incoming_hook({"text": "`request cookie`: {0}\n\n`response cookie` {1}".format( repr(cherrypy.request.cookie), repr(cherrypy.response.cookie) )})
        session_in_cookie = cookie['session_token'].value
        return session_in_cookie, session_from_db

    def user_session(cookie_session_id, mongo_session_id):
        """ fills in the session with user_data #user = cherrypy.session.get('user', None)    """
        user_data = user.find_one({'session_id': {'$in': [cookie_session_id, mongo_session_id]} })
        if not user_data:
            return False # improvise - decide how this error will display itself
        for role in user_data['permissions']:
            cherrypy.session['roles'] = role
        cherrypy.session['session_id'] = user_data['session_id']    
        cherrypy.session['user_id'] = user_data['user_id']
        cherrypy.session['email'] = user_data['email']
        cherrypy.session['username'] = user_data['username']
        cherrypy.session['permissions'] = user_data['permissions']  
        return True # determine how to notify of success here.

    def forget_user(_id):
        user_cookie = get_cookie['session_token'].value
        cookies = cherrypy.response.cookie
        cookies['session_token'] = user_cookie
        cookies['session_token']['path'] = "/"
        cookies['session_token']['expires'] = 0
        cookies['session_token']['max-age'] = 0
        forget = user.find_and_modify(query={'session_id': user_cookie}, update={'$set': {'session_id': ''}})
        forget_by_user_id = user.update_one({'user_id': cherrypy.session.get('user_id')}, {'$set': {'session_id': ''}})            
        cherrypy.session.clear()


    def validate_user(fetch=None, reject_msg="Sorry, you need to be logged in to view this page"):
        cherrypy.request.user = -1
        cookie = cherrypy.request.cookie
        session = 'session_token'
        if session in cookie.keys():
            session_id = cookie[session].value        
            user_data = user.find_one({'session_id': session_id})        
            if user_data:
                cherrypy.request.user = user_data['user_id'] # all logged-in validation depends on uid in request
                #cherrypy.incoming_hook({'text': u":dove_of_peace: {0} logged in via user[fc_session_id]\nsession {1}".format(cherrypy.request.uid, cookie), 'username':'fc-login-user'})
                return
        raise cherrypy.HTTPError(401, reject_msg) #cherrypy.bootstrap_page(reject_msg, "Not logged in", 'fbcommons2_loggedout', "", cherrypy.urls_from_context.get_root_urls(cherrypy.url()))



## -- ACTIVATION EMAIL & PASSWORD TOKEN GENERATE SECTION -- ##

    def generate_confirmation_token(self):

        email = self.email
        SECRET_KEY = secret.key
        SECURITY_PASSWORD_SALT = secret.salt
        serializer = URLSafeTimedSerializer(SECRET_KEY)

        return serializer.dumps(email, salt=SECURITY_PASSWORD_SALT)

    def confirm_token(token, expiration=8500):
        SECRET_KEY = secret.key
        SECURITY_PASSWORD_SALT = secret.salt
        serializer = URLSafeTimedSerializer(SECRET_KEY)

        try:
            email = serializer.loads(
                token,
                salt = SECURITY_PASSWORD_SALT,
                max_age = expiration
            )
        except:
            return False
        return email
    
    def check_token(self, token=None):
        if token:
            email = confirm_token(token)
            user = email if email == self.email else None
            return user
        else:
            return False

    def username_reminder(self):
        user_resend = self.email
        if user_resend.get('fullname'):
            fullname = user_resend['fullname']
        else:
            fullname = user_resend['name']
        username = user_resend['name']
        urls = ufc.get_root_urls(cherrypy.url())

        return email_token(fullname, email, username, mandrill_content_id=11) #change mandrill to other email engine

    def change_password(user_id, password=None):
        if password:
            user = user_db.find_one({'user_id': user_id})
            if user: 
                password = valid_password(password)
                hashpass = encrypt_password(password)
                msg = users.update_one({'user_id':user_id}, {'$set': {'password': hashpass}})
                url = '/admin/dashboard?uid={0}'.format(str(user_id),)
                return {'result_ok': True, 'success_msg': "Your password has been successfully reset. You may login here: <a href='/user/login' class='btn btn-primary'>Login here</a>"}
            else:
                return {'result_ok': False, 'error_msg':"User not found."}
        else:
            return {'result_ok': False, 'error_msg':'Password cannot be blank.'}

### --- Helpers for User Model  --- ###


## -- CRUD functions outside model for Controller -- ##

def get_all_users():
    all_users = user_db.find({'activated':True})
    return all_users

