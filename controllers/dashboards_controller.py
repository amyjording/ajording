import cherrypy, json
from model.dashboard import *
from controllers.sessions_controller import validate

cherrypy.tools.validate = cherrypy.Tool('before_handler', validate(fetch=None))


#@cherrypy.tools.validate(fetch=None)

class DashboardController(object):

    @cherrypy.tools.accept(media='text/plain')
    def GET(self):
        dash = verify_dash()
        return dash

    @cherrypy.expose
    @cherrypy.tools.accept(media='text/plain')
    def PUT(self, pinit=None, item=None):
        dash = verify_dash()
        if dash:
            if pinit == 'pin':
                msg = dash.pin(item)
                if msg:
                    msg = {'result_ok':True, 'success_message':'Pinned!'}
            elif pinit == 'unpin':
                msg = dash.unpin(item)
                if msg:
                    msg = {'result_ok':True, 'success_message':'Unpinned!'}
            else:
                msg = {'result_ok': False, 'error_msg': 'Something went wrong with your pin.'}
            return msg
        else:
            return {'result_ok': False, 'error_msg': 'Something went wrong with your dashboard.'}

    @cherrypy.expose
    @cherrypy.tools.accept(media='text/plain')
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
        return msg
    else:
        return dash