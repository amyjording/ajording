import cherrypy, json
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
        return kw

## -- Managing User credentials -- #

    def identify_user(kw):
        if kw.get('email'):
            email = kw['email'].lower()
            user = User.get_one({'email':email})

            if user:
                if kw.get('senduser') and kw['senduser'] == 'true':
                    info = {'username':user.username}
                    resend(email, info)
                    return {'result_ok':True, 'success_msg': 'Your username has been sent to your email address.'}     
                elif kw.get('resetpass') and kw['resetpass'] == 'true':
                    token = user.generate_confirmation_token()
                    if token:
                        info = {'password': True, 'token':token}
                        resend(email, info) 
                        return {'result_ok':True, 'success_msg': 'A new password token has been sent to your email address.'}
                    else: json.dumps({'result_ok': False, 'error_msg': "The token is invalid or has expired."})

                else:
                    return json.dumps({'result_ok': False, 'error_msg': "Something went wrong. Please contact Amy for help."})
            else:
                return json.dumps({'result_ok': False, 'error_msg':"We could not find your email address."})
        elif kw.get('reset_id'):
                user = check_token(token=kw['reset_id'])
                if user:
                    return json.dumps({'result_ok': True, 'user_id': user._id}) # Need to decide if this is a redirect or ajax form change.
                else:
                    return json.dumps({'result_ok': False, 'error_msg':"Your activation link has expired."})

    def resend(email, kw):
        email = email.lower()
        try:
            this_user = User.get_one({'email':email})
            if this_user.name:
                name = this_user.name
            else:
                name = "Portfolio Fan!"
            email = this_user.email
            url = 'https://www.amyjording.com'
            token = this_user.get_confirmation_token()
                
            if kw.get('username'):
                username = this_user.username
                subject = "Username reminder for AmyJording.com"
                sendgrid_content = f"Hi {name}, your username is {username}. Visit https://www.amyjording.com/demo to login."
                return EmailsController.send_email(email, subject, sendgrid_content)
            
            elif kw.get('password'):
                subject = "Password Reset for AmyJording.com"
                confirm_url = url + '/demo/identify?resettoken={0}'.format(token)
                sendgrid_content = f"Hi {name}, click this link {confirm_url} to confirm this is you and reset your password. If it's not you, simply do nothing."

                return EmailsController.send_email(email, subject, sendgrid_content)
            elif kw.get('activation'):
                subject = "Activate your account at AmyJording.com"
                activation_url = url + '/demo/activation?activatetoken={0}'.format(token)
                sendgrid_content = f"Hi {name}, welcome to Amy's portfolio! Simply click this activation link {activation_url} to complete the sign-up. Thanks!"
                return EmailsController.send_email(email, subject, sendgrid_content) 
            else:
                return "Error, there was nothing to send."
        except pymongo.errors.PyMongoError as e:
            return False


        