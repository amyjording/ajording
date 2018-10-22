import os, os.path
import cherrypy
from view.static import *
from view.work_view import *
from view.demo_view import *
from config.routes import Work
from config.routes import Demo

class Root(object):
	work = Work()
	demo = Demo()
	
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


if __name__ == '__main__':

	cherrypy.config.update({
	'server.socket_host': '127.0.0.1',
	'server.socket_port': 8010,
	'server.thread_pool': 10
	})

	conf = {
		'/': {
			'tools.sessions.on': True,
			'tools.staticdir.root': os.path.abspath(os.getcwd())
		},
		'/static': {
			'tools.staticdir.on': True,
			'tools.staticdir.dir': './public'
			
		},

        '/work' :  {
        	'request.dispatch' : cherrypy.dispatch.MethodDispatcher()
        }

     }
        
	ajording = Root()
	ajording.work = Work()
	ajording.demo = Demo()

cherrypy.tree.mount(ajording, "/", conf)


cherrypy.engine.start()
cherrypy.engine.block()