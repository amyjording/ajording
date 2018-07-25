import cherrypy
import config
from db.mongo import *


def get_portfolios():
	folio = get_db(collection_name=config.collection1)
	portfolios = folio.find()
	return portfolios


def show(portfolio_name):
	folio = get_db(portfolio)
	msg = folio.find_one({'name':portfolio_name})

