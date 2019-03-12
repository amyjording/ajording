import os, os.path
import json
import cherrypy
from config.secrets import secrets
from view.static import *
from view.work_view import *
from view.demo_view import *
from config.routes import *
from controllers.dashboards_controller import *
from controllers.users_controller import authenticate


class Root(object):
	@cherrypy.expose
	def index(self):
		page = index_template()
		return page
	
	@cherrypy.expose
	def about(self):
		page = aboutme_template()
		return page

	@cherrypy.expose
	def contact(self, **kw):
		if kw.get('email') == 'true':
			this_email = secrets()
			my_email = this_email['email']
			return my_email
		page = contactme_template()
		return page

	@cherrypy.expose
	def shutdown(self, **kw):
		if kw.get('wassail') == 'fullsail':
			msg = cherrypy.engine.exit()
		else:
			msg = "Error. Do not pass go."
		return msg

	@cherrypy.expose
	def error_page_404(status, message, traceback, version):
	    return "404 Error!"


if __name__ == '__main__':
	cherrypy.tools.authenticate = cherrypy.Tool('before_handler', authenticate)
	cherrypy.tools.redirect = cherrypy.Tool('before_handler', redirect)
	
	from cherrypy.process.plugins import Daemonizer
	d = Daemonizer(cherrypy.engine)
	d.subscribe()
	
	cherrypy.config.update({
		'global': {
			'environment':'production',
			'server.socket_host': '127.0.0.1',
			'server.socket_port': 8080,
			'server.thread_pool': 30,
			'error_page.404': Root.error_page_404,
			'request.show_tracebacks':True
		}
	})

	conf = {
		'/': {
		'tools.sessions.on': True,
	        'tools.sessions.storage_type': "File",
	        'tools.sessions.storage_class': cherrypy.lib.sessions.FileSession,
	        'tools.sessions.storage_path': "sessions", #"/Users/ADMIN/Python/ajording/sessions",
	        'tools.sessions.timeout' : 129600, # 90 days in minutes
		'tools.staticdir.root': os.path.abspath(os.getcwd())
		},
		'/static': {
			'tools.staticdir.on': True,
			'tools.staticdir.dir': './public'
		}
     }
        
	ajording = Root()
	ajording.work = Work()
	ajording.demo = Demo()
	ajording.dash = Dashboards()
	ajording.update = DashboardController()

cherrypy.tree.mount(ajording, "/", conf)
if hasattr(cherrypy.engine, 'block'):
	cherrypy.engine.start()
	cherrypy.engine.block()
