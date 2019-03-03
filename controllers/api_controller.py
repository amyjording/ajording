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

def advice():
	a = requests.get('http://api.adviceslip.com/advice')
	advice = json.loads(a.text)
	advice = advice['slip']
	image = "/static/images/awesome.jpg"
	advice['image'] = image
	return advice

def pin_advice(slip_id):
	a = requests.get('http://api.adviceslip.com/advice/{0}'.format(slip_id))
	advice = json.loads(a.text)
	advice = advice['slip']
	advice['slip_id'] = slip_id
	image = randomize_image(cat="advice")
	advice['image'] = image
	return advice

def bored():
	r = requests.get('http://www.boredapi.com/api/activity/')
	activity = json.loads(r.text)
	image = randomize_image(cat="bored")
	activity['image'] = image
	return activity

def pin_activity(key):
	r = requests.get('http://www.boredapi.com/api/activity?key={0}'.format(key))
	activity = json.loads(r.text)
	image = "/static/images/adventure.jpg"
	activity['image'] = image
	return activity

def lovecraft(this_id=None):
	wiki = requests.get("https://lovecraft.fandom.com/wiki/Category:Great_Old_Ones")
	soup = BeautifulSoup(wiki.text, 'html.parser')
	links = soup.findAll('a', {'class': 'category-page__member-link'})
	categories = [link.get('title') for link in links]
	if this_id:
		this_old_one = this_id
	else:
		this_old_one = random.choice(categories)
	chosen = wikia.page("Lovecraft", this_old_one)
	try:
		image = chosen.images[0]
	except:
		image = "/static/images/wikia-lc.jpg"
	snippet = (chosen.summary[:100] + '..') if len(chosen.summary) > 100 else chosen.summary
	old_one = {'id': chosen.title, 'title':chosen.title, 'url': chosen.url, 'image': image, 'snippet': snippet}
	# Returns a wiki page, with various specific options to use later.
	# chosen.title will be the title of the Old One page. 
	# chosen.url will be the link to the wiki page
	# chosen.images[0] will yield a string of the url that points to an image. use this to make a daily thumbnail
	# snippet = (chosen.summary[:100] + '..') if len(chosen.summary) > 100 else chosen.summary
	return old_one

def make_id():
	random_letter = random.choice('abcdefxyz')
	random_number = random.randint(1, 999)
	this_id = random_letter+str(random_number)
	return this_id

def randomize_image(cat=None):
	advice = ["https://media.giphy.com/media/mfv1eIC0HAyPe/giphy.gif", "https://media.giphy.com/media/26BRtI7Yk5PJWIfwA/giphy.gif"]
	bored = ["https://media.giphy.com/media/hHCePYCLDqTok/giphy.gif", "https://media.giphy.com/media/3gMbt5JW8JZcbhRzAw/giphy.gif"]
	if cat == "advice":
		random_image = random.choice(advice)
	elif cat == "bored":
		random_image = random.choice(bored)
	else:
		random_image = None
	return random_image