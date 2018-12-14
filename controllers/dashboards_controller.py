import cherrypy, json
from model.dashboard import *


@cherrypy.expose
class DashboardController(object):

    @cherrypy.tools.accept(media='text/plain')
    def GET(self):
    	cherrypy.session['ts'] = time.time()
    	dash = Dashboard()
    	return dash

    def PUT(self, pin_or_unpin=None, **kwarg):
        if pin_or_unpin == 'pin':
            msg = Dashboard.pin(kwarg)
        elif:
            msg = Dashboard.unpin(kwarg)
        else:
            msg = {'result_ok': False, 'error_msg': 'Something went wrong with your pin.'}
        return msg

    def DELETE(self):
        cherrypy.session.pop('ts', None)
        msg = Dashboard.delete()