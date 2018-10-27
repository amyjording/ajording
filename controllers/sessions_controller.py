import cherrypy, json
import pymongo
from db.mongo import get_db
from model.user import *

# this is going to function as both the router and controller 
# controller deals with requests to the database - post put get delete - and confirms permissions.
# the router decides which template to display

class SessionsController(object):


## -- User login & session -- ##

    def login(kw):
        if kw.get('username'):
            submitted = kw['username']
            user = User.get_one({'username':submitted})

            if user:
                password = kw['password'] if kw.get('password') else None
                hashpass = user.encrypt_password(password)
                if user.verify_correct_password(hashpass) is True:
                    user_id = user['_id']
                    user_activated = user['activated']
                    user.set_cookie(user_id)
                    session_in_cookie, session_in_db = remember_user(user_id)
                    user_session(session_in_cookie, session_from_db)
                    return json.dumps({'result_ok': True, 'user_id': user_id, 'activated':user_activated})
                else:
                    return json.dumps({'result_ok': False, 'error_msg':"Incorrect password."})
            else:
                return json.dumps({'result_ok': False, 'error_msg':"We could not find your username."})
        else: 
            return json.dumps({'result_ok': False, 'error_msg':"Please enter a username."})

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


        