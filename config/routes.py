import os, os.path
import cherrypy
from model.user import *
from controllers.users_controller import *
from view.demo_view import *
from view.user_interface import *


class Work(object):

	@cherrypy.expose
	def work(self):
		page = work_template()
		return page


class Demo(object):

##--- USER SECTION -- ##
	status, html = '',''
	content = user_account(status, html)
	page = demo_template(content)

	@cherrypy.expose
	def demo(self):
		msg = "Result of login"
		status, html = user_login_signup()
		page

		if cherrypy.request.method == "POST":
			# need to handle the post
			return page
		return page

	#@cherrypy.expose
	#def show(self, user_id):
	#	page = this_user_template()
	#	return page
	@cherrypy.expose
	def get_in(self, method='GET', **kw):
		if cherrypy.request.method == "POST":
			if kw.get('signin'):
				result = login(kw)
			elif kw.get('signup'):
				result = create(kw)
			if result['result_ok'] is True:
				# redirect to dashboard
				# temporary return
				return """SUCCESS"""
			elif result['result_ok'] is False:
				msg = login_result['msg'] # return a page with danger div showing error message.
				status, html = user_login_signup(msg, alert='danger', collapse='')
				page = demo_template(content)
				return page
			else:
				msg = "Something went wrong."
				status, html = user_login_signup(msg, alert='danger', collapse='')
				page = demo_template(content)
				return page
		else:
			msg = ''
			status, html = user_login_signup(msg)
			page = demo_template(content)
			return page
	
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