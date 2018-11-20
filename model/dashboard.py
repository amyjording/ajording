import os, os.path
import cherrypy,json
import datetime
import pymongo
from cherrypy import request
import sys
sys.path.append('../')

from db.mongo import get_db
from config.secrets import secrets

secret = secrets()
dash_db = get_db(collection_name=secret['collection3'])

class Dashboard(object):

	def __init__(self):
		self.owner = #fetch user through persisted session of user.
		self.taco = #taco API call
		self.bored = #bored API call
		self.lovecraft = #lovecraft API
		self.random = #random API, maybe roll some dice?
		self.sticky = #possible sticky note like a micro post


# to re-run the dashboard to fetch new data from APIs, once a day-ish, use python module schedule
# https://schedule.readthedocs.io/en/stable/ -- use example, place in it's own python file to run.
# refer to this for help: https://stackoverflow.com/questions/15088037/python-script-to-do-something-at-the-same-time-every-day
	
	def refresh(self):
		#this will call all apis that do not have any other interaction but GET
		return
