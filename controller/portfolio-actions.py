import cherrpy
from db.mongo import *

def show(portfolio_name):
	folio = get_db(coll=portfolio)
	msg = folio.find_one({'name':portfolio_name})

