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


    def update(kw):
        user = kw.get('user_token')
        new_password = kw.get('password')
        if user and new_password:
            user = User.get_one({'email':email})
            hashed_new_password = encrypt_password(new_password)
            new_pass = {'password':hashed_new_password}
            results = user.update(new_pass)
        else:
            results = False

        return results

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
                        return {'result_ok':True, 'success_msg': 'A new password token has been sent to your email address.'}
                    else:
                        return {'result_ok': False, 'error_msg': "The token is invalid or has expired."}

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
        return send_email(email, subject, sendgrid_content) 
    else:
        return "Error, there was nothing to send."


def check_token(token=None):
    if token:
        email = confirm_token(token)
        user = User.get_one({'email':email})
        return user
    else:
        return False