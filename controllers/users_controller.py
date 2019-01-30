import cherrypy, json
import requests
import pymongo
from db.mongo import get_db
from model.user import *
from view.demo_view import *
from view.user_interface import *
from controllers.email_controller import *

# this is going to function as both the router and controller 
# controller deals with requests to the database - post put get delete - and confirms permissions.
# the router decides which template to display

class UsersController(object):


## -- Instantiating new user and saving them to database -- ##

    def create(kw):
        username = kw['username']
        email = kw['email'].lower()
        password = kw['password']

        user = User.new(username, email, password) 
        results = user.save()
        #params = {'name':kw['name'], 'email': email, 'password': password, 'username': username}
        return json.dumps(results)

    def GET(*args, **kw):
        user = kw.get('email') or kw.get('_id') or kw.get('username')
        if user:
            if kw.get('email'):
                this_user = User.get_one({'email':kw['email']})
            elif kw.get('_id'):
                this_user = User.get_one({'_id':kw['_id']})
            elif kw.get('username'):
                this_user = User.get_one({'username': kw['username']})
        else:
            user = cherrypy.session.get('_id', None)
            this_user = User.get_one({'_id':user})
        return this_user

    def put(kw):
        user_email = kw.get('usertoken')
        new_password = kw.get('password')
        if user_email and new_password:
            user = User.get_one({'email':user_email})
            hashed_new_password = encrypt_password(new_password)
            new_pass = {'password':hashed_new_password}
            results = user.update(new_pass)
            if results:
                return json.dumps({'result_ok':True, 'success_msg':"Your account has been updated."})
            else:
                return json.dumps({'result_ok':False, 'error_msg':"We couldn't update your account."})
        elif kw.get('activated'):
            user = User.get_one({'_id':kw.get('_id','')})
            if user:
                activated = user.update({'activated':True})
                return True
            else:
                return json.dumps({'result_ok': False, 'error_msg':"We couldn't update your account."})
        else:
            results = json.dumps({'result_ok':False, 'error_msg':"Oops."})
        return results

    def destroy(kw):
        user = User.get_one({'email':kw.get('email','')})
        if user:
            delete_result = user.delete_user()
            if delete_result == True:
                cherrypy.session.clear()
                return True
            else:
                return json.dumps({'result_ok':False, 'error_msg':"Something went wrong. Try again or contact Amy for help."})


## -- Managing User credentials -- #

    def identify_user(self, kw):
        if kw.get('email'):
            email = kw['email'].lower()
            user = User.get_one({'email':email})

            if user:
                if kw.get('resend') == 'senduser':
                    info = {'username': True}
                    msg = resend(user, info)
                    if msg == 202:
                        return {'result_ok':True, 'success_msg': 'Your username has been sent to your email address.'}
                    else:
                        return {'result_ok':False, 'error_msg': 'We could not resend your username. Please contact Amy for help.'}    
                elif kw.get('resend') == 'resetpass':
                    token = user.generate_confirmation_token()
                    info = {'password': True, 'token':token}
                    msg = resend(user, info)
                    if msg == 202:
                        return {'result_ok':True, 'success_msg': 'A new password link has been sent to your email address.'}
                    else:
                        return {'result_ok': False, 'error_msg': "Something went wrong in resending your link."}
                elif kw.get('resend') == 'activation':
                    token = user.generate_confirmation_token()
                    info = {'activation': True, 'token':token}
                    msg = resend(user, info)
                    if msg == 202:
                        return {'result_ok':True, 'success_msg': 'A new activation link has been sent to your email address.'}
                    else:
                        return {'result_ok': False, 'error_msg': "Something went wrong in trying to resend your link."}
                else:
                    return {'result_ok': False, 'error_msg': "Something went wrong. Please contact Amy for help."}
            else:
                return {'result_ok': False, 'error_msg':"We could not find your email address."}
        elif kw.get('resettoken'):
                user = check_token(token=kw['resettoken'])
                if user:
                    return {'result_ok': True, 'user_id': user.email} # Need to decide if this is a redirect or ajax form change.
                else:
                    return {'result_ok': False, 'error_msg':"Your activation link has expired."}

## User Activation, Password Reset, and Username reminders ##

def resend(user, info):
    email = user.email
    name = user.name or "Portfolio Fan"
    url = 'https://www.amyjording.com'
        
    if info.get('username'):
        username = user.username
        subject = "Username reminder for AmyJording.com"
        sendgrid_content = f"Hi {name}, your username is {username}. Visit https://www.amyjording.com/demo to login."
        return send_mail(email, subject, sendgrid_content)
    
    elif info.get('password'):
        subject = "Password Reset for AmyJording.com"
        confirm_url = url + '/demo/change-password?resettoken={0}'.format(info['token'])
        sendgrid_content = f"Hi {name}, click this link {confirm_url} to confirm this is you and reset your password. If it's not you, simply do nothing."
        return send_mail(email, subject, sendgrid_content)

    elif info.get('activation'):
        subject = "Activate your account at AmyJording.com"
        activation_url = url + '/demo/activation?activatetoken={0}'.format(info['token'])
        sendgrid_content = f"Hi {name}, welcome to Amy's portfolio! Simply click this activation link {activation_url} to complete the sign-up. Thanks!"
        return send_mail(email, subject, sendgrid_content) 
    else:
        return "Error, there was nothing to send."


def check_token(token=None):
    if token:
        email = confirm_token(token)
        user = User.get_one({'email':email})
        return user
    else:
        return False

## -- Authentication

@cherrypy.tools.register('before_handler')
def authenticate():
    cookie = cherrypy.request.cookie
    check_for_token = cookie.get('session_token', None)
    if check_for_token:
        session_token = cookie['session_token'].value
        # fc_session_id = bcrypt.hashpw(session_token.encode('utf-8'), bcrypt.gensalt()) # session_token 
        user_from_session = user.get_one({'session_id': session_token})
        if not user_from_session:
            raise cherrypy.HTTPError(404)