import cherrpy
from datetime import datetime
from pymongo import MongoClient


def insert_portfolio_record(dictionary):
	#mongo entry - {'title': 'title goes here', 'created_at': datetime, 'image': 'url here', 'body':'text context'}
	client = MongoClient()
    db = client.arj_database
    collection = db.portfolio

    try:
    	name = dictionary['name'] # unique identifier - not id number
    	title = dictionary['title']
    	summary = dictionary.get('summary', '')
    	body = dictionary['body']
    	image = dictionary['image']
    except:
    	return "Error - You're missing some required fields. Please review and submit again."

    insert_portfolio_data = {
    		u'name': name,
    		u'title': title,
    		u'summary': summary,
    		u'body': body,
    		u'image': image,
    		u'created': datetime.now()
    }

    msg = collection.insert_one(insert_portfolio_data)