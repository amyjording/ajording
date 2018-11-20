import requests
import cherrypy
import json
import wikia
from bs4 import BeautifulSoup
import random
from db.mongo import *


#api calls - store api keys in api collection
#apis = get_db(the api collection here)

def tacofancy():
	t = requests.get('http://taco-randomizer.herokuapp.com/random/')
	recipe = json.loads(t.text)
	return recipe

#bored api call
# GET
def bored():
	r = requests.get('http://www.boredapi.com/api/activity/')
	activity = json.loads(r.text)
	return activity


def lovecraft():
	wiki = requests.get("https://lovecraft.fandom.com/wiki/Category:Great_Old_Ones")
	soup = BeautifulSoup(wiki.text, 'html.parser')
	links = soup.findAll('a', {'class': 'category-page__member-link'})
	categories = [link.get('title') for link in links]
	old_one = random.choice(categories)
	chosen = wikia.page("Lovecraft", old_one)

	# Returns a wiki page, with various specific options to use later.
	# chosen.title will be the title of the Old One page. 
	# chosen.url will be the link to the wiki page
	# chosen.images[0] will yield a string of the url that points to an image. use this to make a daily thumbnail
	# snippet = (chosen.summary[:100] + '..') if len(chosen.summary) > 100 else chosen.summary
	return chosen
	


