import cherrypy
from config.secrets import *
from db.mongo import *
from view.work_view import *

secret = secrets()
folio = get_db(collection_name=secret['collection1'])

def get_portfolios():
	portfolios = folio.find()
	return portfolios

def show(portfolio_name):
	this_portfolio = folio.find_one({'name':portfolio_name})
	return this_portfolio
