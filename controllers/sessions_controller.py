import cherrypy, json
import pymongo
from db.mongo import get_db
from model.user import *

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

    def validate():
        cherrypy.request.user = -1
        cookie = cherrypy.request.cookie
        session = 'session_token'
        if session in cookie.keys():
            session_id = cookie[session].value        
            user_data = user.get_one({'session_id': session_id})        
            if user_data:
                cherrypy.request.user = user_data['user_id']
                return cherrypy.request.user
        else:
            return False


        