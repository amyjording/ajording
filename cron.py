import requests
import datetime
import json
from controllers.api_controller import *
from db.mongo import get_db
from config.secrets import secrets

secret = secrets()
api_db = get_db(collection_name=secret['collection4'])

advice = advice()
activity = bored()
old_one = lovecraft()
this_record = api_db.find_one()
if this_record:
	this_id = this_record['_id']
	msg = api_db.update_one({'_id':this_id},{'$set':{'advice':advice, 'activity':activity, 'old_one':old_one}})
	print(True)
else:
	msg = api_db.insert_one({'advice':advice, 'activity':activity, 'old_one':old_one})
	print("New insert")