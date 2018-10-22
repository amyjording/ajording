import cherrypy, json
import pymongo
from db.mongo import get_db
from model.user import *
from view.demo_view import *
from view.user_interface import *

# this is going to function as both the router and controller 
# controller deals with requests to the database - post put get delete - and confirms permissions.
# the router decides which template to display

class UsersController(object):


## -- Instantiating new user and saving them to database -- ##

    def create(kw):
        username = kw['username']
        email = kw['email'].lower()
        password = kw['password']
        name = kw['name']

        user = User.new(username, email, password, name) 
        results = user.save()
        #params = {'name':kw['name'], 'email': email, 'password': password, 'username': username}
        if results == True:             
            return json.dumps({'result_ok': True, 'username': user.username, 'email': user.email, 'success_msg':"Please check your email to verify your account."})
        else:
            return json.dumps(results['error_msg'])


    def update(kw):
        return kw

## -- User login & session -- ##

    def login(kw):
        submitted_username = kw['username']
        if submitted_username:
            user = User()
            user = user.get(submitted_username)

            if user:
                password = kw['password']
                hashpass = encrypt_password(password)
                if verify_correct_password(password, hashpass) is True:
                    user_id = user['_id']
                    email_validated = user['validated']
                    if email_validated is False:
                        return {'result_ok': False, 'error_msg':"Please check your email and confirm your account through the activation link!</div>"}
                    set_cookie(user_id)
                    session_in_cookie, session_in_db = remember_user(user_id)
                    user_session(session_in_cookie, session_from_db)
                    return json.dumps({'result_ok': True, 'user_id': user_id})
                else:
                    return json.dumps({'result_ok': False, 'error_msg':"Incorrect password."})
            else:
                return json.dumps({'result_ok': False, 'error_msg':"We could not find your username."})
        else: 
            return json.dumps({'result_ok': False, 'error_msg':"Please enter a username."})

## -- Managing User credentials -- #

    def identify_user(kw):
        if kw.get('email'):
            email = kw['email'].lower()
            user = User.get({'email':email})

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
        this_user = User.get({'email':email})
        if this_user.name:
            name = this_user.name
        else:
            name = "Portfolio Fan!"
        url = 'https://amyjording.com'
        sendgrid_content = 'Temporary content. Email content should live somewhere. Maybe in a collection.'
        
        if kw.get('username'):
            username = this_user.username
            return email_token(name, email, username, sendgrid_content)
        elif kw.get('password'):
            token = kw['token']
            confirm_url = url + '/demo/identify?resettoken={0}'.format(token)
            return email_token(name, email, confirm_url, sendgrid_content)
        elif kw.get('activation'):
            token = kw['token']
            activation_url = url + '/demo/activation?activatetoken={0}'.format(token)
            return email_token(name, email, activation_url, sendgrid_content) 
        else:
            return "Error, there was nothing to send."


        