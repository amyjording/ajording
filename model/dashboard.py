import os, os.path
import cherrypy,json
import datetime
import pymongo
from cherrypy import request
import sys
sys.path.append('../')

from db.mongo import get_db
from config.secrets import secrets
from controllers.api_controller import *

secret = secrets()
dash_db = get_db(collection_name=secret['collection3'])

class Dashboard(object):

	def __init__(self, owner):
		self.owner = owner #User instance pass through at login
		self.taco = tacofancy()
		self.bored = bored()
		self.lovecraft = lovecraft()


# to re-run the dashboard to fetch new data from APIs, once a day-ish, use python module schedule
# https://schedule.readthedocs.io/en/stable/ -- use example, place in it's own python file to run.
# refer to this for help: https://stackoverflow.com/questions/15088037/python-script-to-do-something-at-the-same-time-every-day
	
	def refresh(self):
		#this will call all apis that do not have any other interaction but GET
		return

	def initialize(self):

        pin_data = {
                u'owner': self.owner,
                u'taco': [],
                u'bored':[],
                u'lovecraft':[],
                u'deleted': False
                }

        try:
        	save_pin = dash_db.insert_one(pin_data)
            return {'result_ok': True}
        except:
            return {'result_ok': False, 'error_msg': 'Something went wrong with initializing dashboard record.'}

    def pin(self, pin_this=None):
    	if pin_this == 'taco':
    		push_this = {u'taco':self.taco}
    	elif pin_this == 'bored':
    		push_this = {u'bored':self.bored}
    	elif pin_this == 'lovecraft':
    		push_this = {u'lovecraft':self.lovecraft}
    	else:
    		return False
        try:
            try_pin = dash_db.update_one({'_id': self._id}, {'$push': push_this})
            if try_pin.matched_count > 0:
                return True
        except pymongo.errors.PyMongoError as e:
            return False

    def unpin(self, unpin_this=None):
    	if unpin_this == 'taco':
    		pull_this = {u'taco':self.taco}
    	elif unpin_this == 'bored':
    		pull_this = {u'bored':self.bored}
    	elif unpin_this == 'lovecraft':
    		pull_this = {u'lovecraft':self.lovecraft}
    	else:
    		return False
        try:
            try_pin = dash_db.update_one({'_id': self._id}, {'$pull': pull_this})
            if try_pin.matched_count > 0:
                return True
        except pymongo.errors.PyMongoError as e:
            return False