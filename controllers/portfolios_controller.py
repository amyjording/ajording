import cherrypy
import secrets
from db.mongo import *
from view.work_view import *

class PortfoliosController(object):
	folio = get_db(collection_name=secrets.collection1)

	def get_portfolios():
		portfolios = folio.find()
		return portfolios

	def show():
		this_portfolio = folio.find_one({'name':portfolio_name})
		return this_portfolio
