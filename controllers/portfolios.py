import cherrypy
import config
from db.mongo import *

secret = secrets()
folio = get_db(collection_name=secret['collection1'])

def get_portfolios():
	portfolios = folio.find()
	return portfolios


def show(portfolio_name):
	folio = get_db(portfolio)
	msg = folio.find_one({'name':portfolio_name})

