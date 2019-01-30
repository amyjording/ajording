import os, os.path
import cherrypy,json
import datetime
import pymongo
import bcrypt
from cherrypy import request
from random import getrandbits
from base64 import urlsafe_b64encode
from hashlib import sha256
from itsdangerous import URLSafeTimedSerializer
import sys
sys.path.append('../')

from db.mongo import get_db
from config.secrets import secrets

secret = secrets()
user_db = get_db(collection_name=secret['collection2'])
#later project - mongo schema validation could reduce several lines of code
#https://stackoverflow.com/questions/46569262/does-pymongo-have-validation-rules-built-in
#refer to this for reminder emails: https://app.sendgrid.com/guide/integrate/langs/python

class User(object):

    #reference this!! -- https://codereview.stackexchange.com/questions/161340/models-in-a-simple-pymongo-based-blogging-web-app-without-orm-odm
    # no date needed if default id: https://stackoverflow.com/questions/3778428/best-way-to-store-date-time-in-mongodb
    
    def __init__(self, _id=None, username=None, email=None, password=None, 
                name=None, activated=False, session_id=u'', last_login=None,
                ip=u'', following=[], followers=[] ):
             
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

## -- User Model functions for Controller to use -- ##

    @classmethod
    def new(cls, username, email, password):
        ip = cherrypy.request.headers.get("X-Forwarded-For",'0.0.0.0')
        return cls(username=username, email=email, password=password, ip=ip)

    @classmethod
    def get_one(cls, kw):
        if kw.get('_id'):
            this_user = user_db.find_one({'_id': kw['_id']})
        elif kw.get('email'):
            this_user = user_db.find_one({'email': kw['email']})
        elif kw.get('username'):
            this_user = user_db.find_one({'username': kw['username']})
        elif kw.get('session_id'):
            this_user = user_db.find_one({'session_id': kw['session_id']})
        else:
            this_user = False
        if this_user:
            return cls(_id=this_user['_id'], username=this_user['username'], email=this_user['email'], 
                        password=this_user['password'], name=this_user['name'], activated=this_user['activated'], 
                        session_id=this_user['session_id'], ip=this_user['ip'], following=this_user['following'], 
                        followers=this_user['followers'])
        else:
            return False

    def update(self, dictonary_of_records_to_update):
        try:
            update_status = user_db.update_one({'_id': self._id}, {'$set': dictonary_of_records_to_update})
            if update_status.matched_count > 0:
                return True
        except pymongo.errors.PyMongoError as e:
            return False
    
    def delete_user(self):
        try:
            delete = user_db.delete_one({'_id':self._id})
            if delete.matched_count > 0:
                return True
        except pymongo.errors.PyMongoError as e:
            return False

## -- Before Saving New User, verify these inputs -- ##

    def check_unique_credentials(self):
        existing_email = user_db.find_one({'email': self.email})
        existing_username = user_db.find_one({'username': self.username})
        return existing_email, existing_username

    def valid_email(self):
        import re
        check_email = re.match(r'\A[\w+\-.]+@[a-z\d\-]+(\.[a-z\d\-]+)*\.[a-z]+', self.email, flags=0)

        if check_email:
            check_email_length = check_length(check_email.group(0), max=255)
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
            check_username_length = check_length(check_username.group(0), max=60)
            if check_username_length == self.username:
                return True
            else:
                return False
        else:
            return False

    def valid_password(self):
        import re
        password = self.password

        has_upper_case = re.search(r'[A-Z]+', password, flags=0)
        has_lower_case = re.search(r'[a-z]+', password, flags=0)
        has_numbers = re.search(r'\w[0-9]', password, flags=0)
        has_non_alphas = re.search(r'\W', password, flags=0)

        if has_upper_case and has_lower_case and has_numbers and has_non_alphas and len(password) >= 8:
            return True
        else:
            return False

    def before_save(self):
        if not self.username:
            return {'result_ok': False, 'entry': 'username', 'error_msg':'Username cannot be blank.'}

        if not self.password:
            return {'result_ok': False, 'entry': 'password', 'error_msg':'Password cannot be blank.'}

        if not self.email: # bare minimum
            return {'result_ok': False, 'entry': 'email', 'error_msg':'Email cannot be blank.'}
        
        existing_email, existing_username = self.check_unique_credentials()

        if existing_email:
            return {'result_ok': False, 'entry': 'email', 'error_msg': 'This email already has an account, please Sign in.'}
        elif existing_username:
            return {'result_ok': False, 'entry': 'username', 'error_msg': 'This username has already been taken. Please choose another username.'}

        if self.valid_email() is False:
            return {'result_ok': False, 'entry': 'email', 'error_msg':'Please enter a valid email.'}

        if self.valid_username() is False:
            return {'result_ok': False, 'entry': 'username', 'error_msg':'Please enter a valid username.'}
        
        if self.valid_password() is False:
            return {'result_ok': False, 'entry': 'password', 'error_msg':'Please choose a password that is at least 8 characters long, at least one uppercase letter, one lowercase letter, a number, and a symbol.'}
        else:
            return True    

## SAVE NEW USER
    def save(self):
        try_save = self.before_save() 
        if try_save == True: 
        
            hashpass = encrypt_password(self.password)    
            
            if self.name:
                if check_length(self.name, max=255):
                    name = self.name
            else:
                name = 'Portfolio Tourist'

            imported_user_data = {
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
            
            return {'result_ok': True, 'email': self.email, 'name': self.username, 'password':self.password, 'hashed': hashpass, 'success_msg':"Please check your email to verify your account."}
        else:
            return {'result_ok': False, 'entry': try_save['entry'], 'error_msg': try_save['error_msg']}

## ------------ END CREATE USER -------------##


## ---------- User Login, Session and Logout -------- ##

    def validate_password(self, submitted_password):
        hashedpass = self.password
        if bcrypt.hashpw(submitted_password.encode('utf-8'), hashedpass) == hashedpass:
            return True
        else:
            return False

    def set_cookie(self):
        expiration = datetime.datetime.now() + datetime.timedelta(days=90)
        self.session_id = str(gen_key())
        update_user_session = self.update({'session_id': self.session_id})
        set_cookies = cherrypy.response.cookie
        set_cookies['session_token'] = self.session_id
        set_cookies['session_token']['path'] = "/"
        #set_cookies['session_token']['domain'] = "amyjording.com"
        set_cookies['session_token']['expires'] = \
            expiration.strftime("%a, %d-%b-%Y %H:%M:%S UTC")
        return str(set_cookies['session_token'].value)

    def remember_user(self, cookie):
        session_from_db = User.get_one({'session_id':cookie})

        if session_from_db:
            this_ip = cherrypy.request.headers.get("X-Forwarded-For",'0.0.0.0')
            update_user_session_data = self.update({'last_login': datetime.datetime.utcnow(),'ip': this_ip})
            return True
        else:
            return session_from_db, cookie

    def user_session(self):
        cherrypy.session['session_id'] = self.session_id   
        cherrypy.session['_id'] = self._id
        cherrypy.session['email'] = self.email
        cherrypy.session['username'] =self.username
        return True

    def login_user(self, submitted_password):
        password = submitted_password
        if self.validate_password(password) is True:
            cookie = self.set_cookie()
            msg = self.remember_user(cookie)
            if msg:
                self.user_session()
                return json.dumps({'result_ok': True})
            else:
                return json.dumps({'result_ok': False, 'type':'session', 'error_msg':'We had a session mismatch. Please try again.'})
        else:
            return json.dumps({'result_ok': False, 'type': 'password', 'error_msg':"Incorrect password."})
            
    def forget_user(self):
        user_cookie = get_cookie['session_token'].value
        cookies = cherrypy.response.cookie
        cookies['session_token'] = user_cookie
        cookies['session_token']['path'] = "/"
        cookies['session_token']['expires'] = 0
        cookies['session_token']['max-age'] = 0
        if self._id != cherrypy.session.get('_id'):
            forget = user_db.update_one({'_id': cherrypy.session.get('_id')}, {'$set': {'session_id': ''}})
        else:
            forget = self.update({'session_id': ''})         
        cherrypy.session.clear()



## -- ACTIVATION EMAIL & PASSWORD TOKEN GENERATE SECTION -- ##

    def generate_confirmation_token(self):
        email = self.email
        SECRET_KEY = secret['key']
        SECURITY_PASSWORD_SALT = secret['salt']
        serializer = URLSafeTimedSerializer(SECRET_KEY)
        return serializer.dumps(email, salt=SECURITY_PASSWORD_SALT)

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

def check_length(text, max=60): 
    text = text[:max] 
    return text

def expire_user_cookies(session_cookie):
    cookies = cherrypy.response.cookie
    cookies['session_token'] = session_cookie
    cookies['session_token']['path'] = "/"
    cookies['session_token']['expires'] = 0
    cookies['session_token']['max-age'] = 0

## -- CRUD functions outside model for Controller -- ##

def get_all_users():
    all_users = user_db.find({'activated':True})
    return all_users

## -- Encryption and Random key generators -- ##

def encrypt_password(password):
    import bcrypt
    hashpass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashpass

def gen_key():
   keyLenBits = 64
   a = str(getrandbits(keyLenBits)).encode('utf-8')
   b = urlsafe_b64encode(sha256(a).digest())
   return b

def confirm_token(token, expiration=8500):
    SECRET_KEY = secret['key']
    SECURITY_PASSWORD_SALT = secret['salt']
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

