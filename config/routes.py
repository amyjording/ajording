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
from jinja2 import Environment, PackageLoader, select_autoescape, Markup
env = Environment(
loader=PackageLoader('ajording', 'view/templates'),
autoescape=select_autoescape(['html', 'xml'])
)


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
		msg = " "
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
			if result.get('result_ok') == True:
				user = UsersController.GET({'email':result['email']})
				keys = {'email': result['email'], 'resend':'activation'}
				send_activation = UsersController.identify_user(keys)
				user_login = SessionsController.create({'email':result['email'], 'password':result['password']})
				init_user_dash = DashboardController.create(user)
				return user_login
			else:
				return json.dumps(result)
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
		token = get_cookie()
		if not cherrypy.session.get('_id') or not token:
			msg = 'You are not logged in. You may login here:'
			status, html = user_login_signup(msg)
			content = user_account(status, html)
			page = demo_template(content)
			return page		
		else:
			msg = SessionsController.destroy()
			status, html = user_login_signup(msg.get('success_msg') or msg.get('error_msg'))
			content = user_account(status, html)
			page = demo_template(content)
		return page

	@cherrypy.expose
	def settings(self, method='GET', **kw):

		if cherrypy.request.method == 'POST':
			response = UsersController.put(kw)
			return json.dumps(response)
		else:
			page_list = ['about', 'work', 'demo', 'contact']
			urls = cherrypy.url()
			msg = ''
			kw = {'cookie':True}
			user = UsersController.GET(kw)
			template = env.get_template('settings.html')
		return template.render(page_list=page_list, urls=urls, msg=msg, user=user)
			

	@cherrypy.expose
	def identify(self, method='GET', **kw):
		if cherrypy.request.method == 'POST':
			result = UsersController.identify_user(kw)
			return json.dumps(result)
		elif kw.get('resettoken'):
			result = UsersController.identify_user(kw)
			if result.get('result_ok') == True:
				status, html = user_reset_password(result['user_id'])
		elif kw.get('resend') == 'activation':
			result = UsersController.identify_user(kw)
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
	def change_password(self, method='GET', **kw):
		response = alert = msg = link = button = page = ''

		if cherrypy.request.method == 'POST':
			response = UsersController.put(kw)
			if response['result_ok'] == True:
				alert = 'success'
				msg = response['success_msg']
				link = "/demo"
				button = 'Sign in here'
			else:
				alert = 'danger'
				msg = response['error_msg']
				link = '/demo/identify'
				button = 'Recover your username or password here.'
			status, html = reset_results(alert, msg, link, button)
			content = user_account(status, html)
			page = demo_template(content)
			return page
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
				raise cherrypy.HTTPRedirect("/dash")				
		else:
			raise cherrypy.HTTPError(404)

	@cherrypy.expose
	def delete(self, **kw):
		destroy_dashboard = DashboardController.DELETE()
		deleted_result = UsersController.destroy(kw)

		if deleted_result == True:
			msg = SessionsController.destroy()
			raise cherrypy.HTTPRedirect("/")
		else:
			msg = deleted_result['error_msg']
			page_list = ['about', 'work', 'demo', 'contact']
			urls = cherrypy.url()
			kw = {'cookie':True}
			user = UsersController.GET(kw)
			template = env.get_template('settings.html')
			return template.render(page_list=page_list, urls=urls, user=user, msg=msg)



class Dashboards(object):

	@cherrypy.expose
	@cherrypy.tools.authenticate()
	def index(self):
		page_list = ['about', 'work', 'dash', 'contact']
		urls = cherrypy.url()
		owner = UsersController.GET({'_id':cherrypy.session.get('_id', None)})
		if owner:
			if owner.activated == False:
				link = Markup(f'<a href="/demo/identify?resend=activation&email={owner.email}" class="btn btn-primary label-bold">click here</a>')
				msg = f"Please check your email to activate your account. If you need a new activation link, please {link}."
				not_activated_template = env.get_template('dash_unactivated.html')
				return not_activated_template.render(page_list=page_list, urls=urls, msg=msg)
		else:
			return cherrypy.session.get('_id', None)
		dash = DashboardController.GET(self)
		template = env.get_template('dashboard.html')
		return template.render(page_list=page_list, urls=urls, dash=dash)


""" helper functions to test cookies and sessions:

	@cherrypy.expose
	def get_cookie(self):
		cookie = cherrypy.request.cookie
		cookie = cookie.get('session_token')
		cookie = cookie.value
		return cookie

	@cherrypy.expose
	def get_session(self):
		user = cherrypy.session.get('username', None)
		return user

	@cherrypy.expose
	def setter(self):
		email = "email@email.com"
		cherrypy.session["email"] = email
		return 'Variable stored in session object. Now check out the <a href="/demo/getter">getter function</a>'

	@cherrypy.expose
	def getter(self):
		return "The email you set earlier, was " + cherrypy.session.get("email")

	@cherrypy.expose
	def delete_cookie(self):
		cookie = "b'7KIYIvvDiIBgMeYl64AYzpG45k3ihMCmvv9gpGH4rWc='"
		cookies = cherrypy.response.cookie
		cookies['session_token'] = cookie
		cookies['session_token']['path'] = "/"
		cookies['session_token']['expires'] = 0
		cookies['session_token']['max-age'] = 0
		return cookies 

		@cherrypy.expose
	def check_pass(self, **kw):
		user = UsersController.GET(kw)
		if user:
			password = kw['password']
			msg = user.validate_password(password)
			if msg:
				return "Victory!"
		else:
			msg = "No go"
		return msg """