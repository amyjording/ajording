import cherrypy, json
import os, os.path
import sys
sys.path.append('../')

from model.user import *
from controllers.users_controller import *
from controllers.sessions_controller import *
from view.demo_view import *
from view.work_view import *
from view.user_interface import *


class Work(object):

	@cherrypy.expose
	def index(self):
		page = work_template()
		return page


class Demo(object):

##--- USER SECTION -- ##

	@cherrypy.expose
	def index(self):
		msg = "Signin or Signup"
		status, html = user_login_signup(msg=msg)
		content = user_account(status, html)
		page = demo_template(content)

		if cherrypy.request.method == "POST":
			# need to handle the post
			msg = "Result of loggin in or signing up"
			
		return page

	#@cherrypy.expose
	#def show(self, user_id):
	#	page = this_user_template()
	#	return page
	@cherrypy.expose
	def get_in(self, method='GET', **kw):
		msg = 'Signin or Signup'
		status, html = user_login_signup(msg=msg)
		content = user_account(status, html)
		page = demo_template(content)
		return page

	@cherrypy.expose
	def signup(self, method='GET', **kw):
		if cherrypy.request.method == 'POST':
			result = UsersController.create(kw)
			return result
		else:
			return 'Something weird happened.'

	@cherrypy.expose
	def login(self, method='GET', **kw):
		if cherrypy.request.method == 'POST':
			result = SessionsController.create(kw)
			return result
		else:
			return json.dumps({'error_msg':'Something weird happened.'})


	
	@cherrypy.expose    
	def signout(self):
		get_cookie = cherrypy.request.cookie
		if not cherrypy.session.get('user_id') or not get_cookie.get('session_token'):
			msg = 'You are not logged in. You may login here:'
			status, html = user_logout(msg)
			page = demo_template(content)
			return page		
		else:
			forget_user(user_id, user_cookie)
			msg = "You have been logged out. Login again here:"
			status, html = user_logout(msg)
			page = demo_template(content)
		return page

	@cherrypy.expose
	def identify(self, method='GET', **kw):
		if cherrypy.request.method == 'POST':

			result = identify_user(kw)
			if result['result_ok'] == True:
				if result.get('success_msg'):
					msg = result['success_msg']
					success = 'success'
					collapse = 'in'
					status, html = user_login_recover_form(msg, success, collapse)
					page = demo_template(content)
				else:
					status, html = invalid_token()
					page = demo_template(content)
		else:
			status, html = user_login_recover_form()
			page = demo_template(content) 

	@cherrypy.expose
	def change_password(self, method='GET', user_token=None):
		if kw['user_token']:
			user = check_token(reset_id=kw['user_token'])
			if user:
				user_id = user['user_id']
				password = kw['password']
				msg = change_password(user_id, password=password)
				status, html = user_reset_password(kw['user_token'])
				page = demo_template(content)
		else:
			status, html = invalid_token()
			page = demo_template(content)	

@cherrypy.expose
class Dashboard(object):

    @cherrypy.tools.accept(media='text/plain')
    def GET(self):
    	cherrypy.session['ts'] = time.time()
    	msg = collection.find_one({'session_id':cherrypy.session.id})
    	return msg['value']

    def POST(self, length=8):
        some_string = ''.join(random.sample(string.hexdigits, int(length)))
        msg = collection.insert_one({'session_id':cherrypy.session.id, 'value': some_string})
        cherrypy.session['ts'] = time.time()
        return some_string

    def PUT(self, another_string):
    	msg = collection.update_one({'session_id':cherrypy.session.id}, {'$set':{'value': another_string}})
    	cherrypy.session['ts'] = time.time()

    def DELETE(self):
        cherrypy.session.pop('ts', None)
        msg = collection.delete_one({'session_id':cherrypy.session.id})