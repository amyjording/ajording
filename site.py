import os, os.path
import cherrypy
from view.static import *
from view.work_view import *
from view.demo_view import *

class AmyJording(object):
	@cherrypy.expose
	def index(self):
		page = index_template()
		return page
	
	@cherrypy.expose
	def about(self):
		page = aboutme_template()
		return page

	@cherrypy.expose
	def work(self):
		page = work_template()
		return page

	@cherrypy.expose
	def demo(self):
		page = demo_template()
		return page

	@cherrypy.expose
	def contact(self):
		page = contactme_template()
		return page



if __name__ == '__main__':
	conf = {
		'/': {
			'tools.sessions.on': True,
			'tools.staticdir.root': os.path.abspath(os.getcwd())
		},
		'/static': {
			'tools.staticdir.on': True,
			'tools.staticdir.dir': './public'
			
		}
	}
	cherrypy.quickstart(AmyJording(), '/', conf)