import cherrypy, json
from model.dashboard import *
from controllers.sessions_controller import validate

cherrypy.tools.validate = cherrypy.Tool('before_handler', validate(fetch=None))

@cherrypy.expose
@cherrypy.tools.validate(fetch=None)
class DashboardController(object):

    @cherrypy.tools.accept(media='text/plain')
    def GET(self):
        dash = verify_dash()
        return dash

    def PUT(self, pin_or_unpin=None, item_id=None):
        dash = verify_dash()
        if dash.get('result_ok'):
            return dash
        if pin_or_unpin == 'pin':
            msg = dash.pin(item_id)
        elif pin_or_unpin == 'unpin':
            msg = dash.unpin(item_id)
        else:
            msg = {'result_ok': False, 'error_msg': 'Something went wrong with your pin.'}
        return msg

    def DELETE(self):
        dash = verify_dash()
        if dash.get('result_ok'):
            return dash
        msg = dash.delete()
        if msg == True:
            msg = {'result_ok': True, 'success_msg':'Dashboard deleted.'}

def verify_dash():
    owner = cherrypy.session.get('_id', None)
    if not owner:
        msg = {'result_ok': False, 'error_msg': 'You are not authorized to do this.'}
        return msg
    dash = Dashboard(owner)
    if not dash:
        msg = {'result_ok': False, 'error_msg': 'This dashboard does not exist.'}
    else:
        msg = dash
    return msg