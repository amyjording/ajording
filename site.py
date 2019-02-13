import os, os.path
import cherrypy
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
	def contact(self):
		page = contactme_template()
		return page

	@cherrypy.expose
	def shutdown(self):
		cherrypy.engine.exit()

	@cherrypy.expose
	def error_page_404(status, message, traceback, version):
	    return "404 Error!"


if __name__ == '__main__':
	from cherrypy._cpnative_server import CPHTTPServer
	cherrypy.server.httpserver = CPHTTPServer(cherrypy.server)
	cherrypy.tools.authenticate = cherrypy.Tool('before_handler', authenticate)
	cherrypy.tools.redirect = cherrypy.Tool('before_handler', redirect)
	cherrypy.server.ssl_certificate = "cert.pem"
	cherrypy.server.ssl_private_key = "privkey.pem"
	cherrypy.config.update({
		'global': {
			'server.socket_host': '127.0.0.1',
			'server.socket_port': 8080,
			'server.thread_pool': 10,
			'error_page.404': Root.error_page_404
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

cherrypy.quickstart(ajording, "/", conf)
