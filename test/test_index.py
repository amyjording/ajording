import cherrypy
from cherrypy.test import helper
from contextlib import contextmanager
 
@contextmanager
def run_server():
    cherrypy.engine.start()
    cherrypy.engine.wait(cherrypy.engine.states.STARTED)
    yield
    cherrypy.engine.exit()
    cherrypy.engine.block()
    
class SimpleCPTest(helper.CPWebCase):
	def setup_server():
		class Root(object):
			@cherrypy.expose
			def echo(self, message):
				return message

		cherrypy.tree.mount(Root())
	setup_server = staticmethod(setup_server)

	def test_index(self):
		self.getPage("/index")
		self.assertStatus('200 OK')
		self.assertHeader('Content-Type', 'text/html')
		self.assertBody('Hello, world\r\n')
		self.getPage("/index")
		self.assertStatus(301)
		self.assertHeader('Location', '%s/docroot/' % self.base())
		self.assertMatchesBody("This resource .* <a href=(['\"])%s/docroot/\\1>"
        						"%s/docroot/</a>." % (self.base(), self.base()))