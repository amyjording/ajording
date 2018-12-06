import cherrypy, json
from model.dashboard import *


@cherrypy.expose
class DashboardController(object):

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