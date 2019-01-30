import cherrypy, json
import requests
import os, os.path
import sys
sys.path.append('../')

from model.user import *
from controllers.users_controller import *
from controllers.sessions_controller import *
from controllers.dashboards_controller import *
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
	@cherrypy.tools.redirect()
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
		cookie = cherrypy.request.cookie['session_token']
		#msg = 'Signin or Signup'
		#status, html = user_login_signup(msg=msg)
		#content = user_account(status, html)
		#page = demo_template(content)
		return cookie
	@cherrypy.expose
	def signup(self, method='GET', **kw):
		if cherrypy.request.method == 'POST':
			result = UsersController.create(kw)
			return result
		else:
			return 'Something weird happened.'

	@cherrypy.expose
	def login(self, method='GET', **kw):
		#if cherrypy.request.method == 'POST':
		result = SessionsController.create(kw)
		return result
		#else:
		#	return json.dumps({'error_msg':'Something weird happened.'})

	
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
	def settings(self, method='GET', **kw):
		if cherrypy.request.method == 'POST':
			response = UsersController.put(kw)
			return response
		else:
			page_list = ['about', 'work', 'demo', 'contact']
			urls = cherrypy.url()
			msg = ''
			user = UsersController.GET()
			template = env.get_template('settings.html')
		return template.render(page_list=page_list, urls=urls, msg=msg, user=user)
			

	@cherrypy.expose
	def identify(self, method='GET', **kw):
		if cherrypy.request.method == 'POST':
			result = UsersController.identify_user(self, kw)
			return json.dumps(result)
		elif kw.get('resettoken'):
			result = UsersController.identify_user(self, kw)
			if result.get('result_ok') == True:
				status, html = user_reset_password(result['user_id'])
		elif kw.get('resend') == 'activation':
			result = UsersController.identify_user(self, kw)
			if result.get('result_ok') == True:
				from jinja2 import Environment, PackageLoader, select_autoescape
				env = Environment(
				loader=PackageLoader('ajording', 'view/templates'),
				autoescape=select_autoescape(['html', 'xml'])
				)

				page_list = ['about', 'work', 'demo', 'contact']
				urls = cherrypy.url()
				owner = UsersController.GET({'_id':cherrypy.session.get('_id', None)})
				msg = f"A new activation link has been emailed to you! Please check your email to activate your account."
				not_activated_template = env.get_template('dash_unactivated.html')	
				return not_activated_template.render(page_list=page_list, urls=urls, msg=msg)
		else:
			status, html = user_login_recover_form()
			content = user_account(status, html)
			page = demo_template(content)
		return page 

	@cherrypy.expose
	@cherrypy.tools.authenticate()
	def change_password(self, method='GET', **kw):
		if cherrypy.request.method == 'POST':
			response = UsersController.put(kw)
			if response:
				alert = 'success'
				msg = "Your password has been reset!"
				link = "/demo"
				button = 'Sign in here.'
				status, html = reset_results(alert, msg, link, button)
				content = user_account(status, html)
				page = demo_template(content)

		elif kw.get('resettoken'):
			user = check_token(token=kw['resettoken'])
			if user:
				user_id = user._id
				status, html = user_reset_password(user.email)
				content = user_account(status, html)
				page = demo_template(content)
		else:
			alert = 'danger'
			msg = "The Password Reset Link is invalid or has expired."
			link = '/demo/identify'
			button = 'Recover your username or password here.'
			status, html = reset_results(alert, msg, link, button)
			content = user_account(status, html)
			page = demo_template(content)	
		return page

	@cherrypy.expose
	def activation(self, method='GET', **kw):
		if kw.get('activatetoken'):
			user = check_token(token=kw['activatetoken'])
			if user:
				user_id = user._id
				kw = {'_id':user_id, 'activated':True}
				activate = UsersController.put(kw)
				if activate == True:
					raise cherrypy.HTTPRedirect("/dash")
				else:
					return json.dumps(activate)
		else:
			raise cherrypy.HTTPError(404)
		return page

	@cherrypy.expose
	def delete(self, **kw):
		deleted_result = UsersController.destroy(kw)
		if deleted_result == True:
			raise cherrypy.HTTPRedirect("https://www.amyjording.com")
		else:
			msg = deleted_result['error_msg']
			page_list = ['about', 'work', 'demo', 'contact']
			urls = cherrypy.url()
			user = UsersController.get()
			template = env.get_template('settings.html')
			return template.render(page_list=page_list, urls=urls, user=user, msg=msg)

class Dashboards(object):

	@cherrypy.expose
	@cherrypy.tools.authenticate()
	def index(self):
		from jinja2 import Environment, PackageLoader, select_autoescape, Markup
		env = Environment(
		loader=PackageLoader('ajording', 'view/templates'),
		autoescape=select_autoescape(['html', 'xml'])
		)

		page_list = ['about', 'work', 'dash', 'contact']
		urls = cherrypy.url()
		owner = UsersController.GET({'_id':cherrypy.session.get('_id', None)})
		if owner:
			if owner.activated == False:
				link = Markup(f'<a href="/demo/identify?resend=activation&email={owner.email}" class="btn btn-primary label-bold">click here</a>')
				msg = f"Please check your email to activate your account. If you need a new activation link, please {link}."
				not_activated_template = env.get_template('dash_unactivated.html')
				return not_activated_template.render(page_list=page_list, urls=urls, msg=msg)
		dash = DashboardController.GET(self)
		template = env.get_template('dashboard.html')
		return template.render(page_list=page_list, urls=urls, dash=dash)

"""			if result['result_ok'] == True:
				if result.get('success_msg'):
					msg = result['success_msg']
					success = 'success'
					collapse = 'in'
					status, html = user_login_recover_form(msg, success, collapse)
					content = user_account(status, html)
					page = demo_template(content)
				else:
					status, html = invalid_token()
					content = user_account(status, html)
					page = demo_template(content)
				return result
			else:
				msg = result.get('error_msg', 'Something happened')
				danger = 'danger'
				collapse = 'in'
				status, html = user_login_recover_form(msg, success, collapse)
				content = user_account(status, html)
				page = demo_template(content)"""