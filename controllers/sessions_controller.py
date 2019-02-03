import cherrypy, json
import pymongo
from db.mongo import get_db
from model.user import *
from controllers.users_controller import get_cookie

# this is going to function as both the router and controller 
# controller deals with requests to the database - post put get delete - and confirms permissions.
# the router decides which template to display

class SessionsController(object):

## -- User login & session -- ##

    def create(kw):
        submitted = kw['email'].lower()
        password = kw['password']
        user = User.get_one({'email':submitted})
        if user:
            results = user.login_user(password)
        else: 
            results = json.dumps({'result_ok': False, 'entry': 'email', 'error_msg': 'This email is not registered. Please sign-up.'})
        return results

    def destroy():
        try:
            token = get_cookie()
            if token:
                this_user = User.get_one({'session_id': token})
                logout = this_user.forget_user()
                cherrypy.session.clear()
                return {'result_ok':True, 'success_msg':'You have been logged out. '}
        except:
            return {'result_ok': False, 'error_msg':"You are not logged in."}

