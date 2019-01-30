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
api_db = get_db(collection_name=secret['collection4'])


class Dashboard(object):

	def __init__(self, owner):
		self.owner = owner #User instance pass through at login
		self.this_dash = dash_db.find_one({'owner':self.owner})
		if not self.this_dash:
			msg = self.initialize()
		self._id = self.this_dash.get('_id', None)
		daily_apis = api_db.find_one()
		self.advice = daily_apis['advice']
		self.bored = daily_apis['activity']
		self.lovecraft = daily_apis['old_one']
		self.pinned_advice = [advice for advice in self.this_dash['advice']]
		self.pinned_bored = [activity for activity in self.this_dash['bored']]
		self.pinned_lovecraft = [this_one for this_one in self.this_dash['lovecraft']]
		# self.taco = tacofancy() - taco response is quite detailed and involved. Maybe later.

# to re-run the dashboard to fetch new data from APIs, once a day-ish, use python module schedule
# https://schedule.readthedocs.io/en/stable/ -- use example, place in it's own python file to run.
# refer to this for help: https://stackoverflow.com/questions/15088037/python-script-to-do-something-at-the-same-time-every-day
	
#	def refresh(self):
		#this will call all apis that do not have any other interaction but GET
#		return

	def initialize(self):
		dash_data = {
				u'owner': self.owner._id,
				u'advice': [],
				u'bored': [],
				u'lovecraft': [],
				u'advice_img': [], # need to put image urls in here for it to work.
				u'bored_img': [],
				u'deleted': False
				}
		try:
			save_dash = dash_db.insert_one(dash_data)
			return True
		except:
			return False


	def pin(self, pin_this):
		if pin_this.startswith('advice'):
			slip_id = pin_this.lstrip('advice-')
			if slip_id not in self.this_dash['advice']:
				push_this = {u'advice': pin_advice(slip_id)}
			else:
				return False
		elif pin_this.startswith('bored'):
			key = pin_this.lstrip('bored-')
			if key not in self.this_dash['bored']:
				push_this = {u'bored': pin_activity(key)}
			else:
				return False
		elif pin_this.startswith('love'):
			this_one = pin_this.lstrip('love-')
			if this_one not in self.this_dash['lovecraft']:
				push_this = {u'lovecraft': lovecraft(this_id=this_one)}
			else:
				return False
		else:
			return False
		try:
			try_pin = dash_db.update_one({'_id': self._id}, {'$push': push_this})
			if try_pin.matched_count > 0:
				return True
		except pymongo.errors.PyMongoError as e:
			return False

	def unpin(self, unpin_this):
		if unpin_this.startswith('advice'):
			slip_id = unpin_this.lstrip('advice-')
			pull_this = {u'advice': {'slip_id': slip_id}}
			pin_length = len(self.pinned_advice)
		elif unpin_this.startswith('bored'):
			key = unpin_this.lstrip('bored-')
			pull_this = {u'bored': {'key':key}}
			pin_length = len(self.pinned_bored)
		elif unpin_this.startswith('love'):
			this_one = unpin_this.lstrip('love-')
			pull_this = {u'lovecraft':{'id':this_one}}
			pin_length = len(self.pinned_lovecraft)
		else:
			return False
		try:
			try_pin = dash_db.update_one({'_id': self._id}, {'$pull': pull_this})
			if try_pin.matched_count < pin_length:
				return True
		except pymongo.errors.PyMongoError as e:
			return False

	def delete(self):
		this_dash = dash_db.update_one({'_id': self._id}, {'$set':{'deleted':True}})
		return True

def randomize_image(kw):
	import random
	random_image = random.choice(kw)
	return random_image