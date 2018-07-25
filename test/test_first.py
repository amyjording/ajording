import cherrypy
from cherrypy.test import helper

class SimpleCPTest(helper.CPWebCase):
	def setup_server():
		class Root(object):
			@cherrypy.expose
			def echo(self, message):
				return message

		cherrypy.tree.mount(Root())
	setup_server = staticmethod(setup_server)

	def test_message_should_be_retuned_as_is(self):
		self.getPage("/echo?message=Hello%20World")
		self.assertStatus('200 OK')
		self.assertHeader('Content-Type', 'text/html;charset=utf-8')
		self.assertBody('Hello World')

	def test_non_utf8_message_will_fail(self):
		self.getPage("/echo?message=A+bient%F4t",
					headers=[
						('Accept-Charset', 'ISO-8859-1,utf-8'),
						('Content-Type', 'text/html;charset=ISO-8859-1')
					]
		)
		self.assertStatus('404 Not Found')