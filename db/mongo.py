from pymongo import MongoClient

def get_db(coll='example'):
	client = MongoClient()
	db = client.arj_database
	collection = db.coll
	return collection