import cherrypy, json
from model.dashboard import *
from controllers.users_controller import *

#@cherrypy.tools.validate(fetch=None)

class DashboardController(object):

    def create(owner):
        dash = Dashboard.new(owner)
        save_dash = dash.initialize(owner._id)
        return save_dash

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

    def DELETE():
        dash = verify_dash()
        msg = dash.delete()
        return msg

def verify_dash():
    owner = UsersController.GET({'cookie':True})
    if not owner:
        msg = {'result_ok': False, 'error_msg': 'You are not authorized to do this.'}
        return msg
    dash = Dashboard.get_one(owner)
    if not dash:
        msg = {'result_ok': False, 'error_msg': 'This dashboard does not exist.'}
        return msg
    else:
        return dash

