import cherrypy, json
import pymongo
from db.mongo import get_db
from model.user import *
from controllers.users_controller import *

# this is going to function as both the router and controller 
# controller deals with requests to the database - post put get delete - and confirms permissions.
# the router decides which template to display

class SessionsController(object):

## -- User login & session -- ##

    def create(kw):
        submitted = kw['email'].lower()
        password = kw['password']
        user = UsersController.GET({'email':submitted})
        if user:
            results = user.login_user(password)
        else: 
            results = json.dumps({'result_ok': False, 'entry': 'email', 'error_msg': 'This email is not registered. Please sign-up.'})
        return results

    def destroy():
        try:
            user_cookie = get_cookie()
            if user_cookie:
                user = UsersController.GET()
                logout = user.forget_user()
                return json.dumps({'result_ok':True})
        except:
            return json.dumps({'result_ok': False, 'error_msg':"You are not logged in."})

