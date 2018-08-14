import cherrypy
from datetime import datetime
import sys
sys.path.append('../')
from db.mongo import *

my_list = [{'name':'fbc', 'title': 'Feedback Commons', 'link': 'https://feedbackcommons.org', 'created_at': datetime, 'image': 'http://arabianglimmer.com/images/fbc.png', 'body':'Custom built User Management system using Cherrypy and Python. <br />Built custom neighborhoods which are dedicated benchmarks of survey response data shared between organizations that share the benchmark averages.', 'tech': ['Python', 'Cherrypy', 'Pymongo/MongoDB', 'MySQL', 'Slack', 'Github', 'API', 'JavaScript/jQuery', 'AJAX', 'Drupal', 'Wordpress', 'Mandrill/Mailchimp', 'SurveyGizmo', 'Bootstrap & LESS', 'D3/svg', 'HTML'], 'primary':'Python', 'display': True}, {'name':'sap','title': 'Sample App', 'link':'https://safe-lowlands-94629.herokuapp.com/', 'created_at': datetime, 'image': 'http://arabianglimmer.com/images/sample_app.png', 'body':'Tutorial Deep Dive follow along, building user management from scratch, microposts, permissions and ability to follow/unfollow.', 'tech': ['Ruby', 'Rails', 'ActiveRecord', 'Carrierwave/ImageMagick', 'Github', 'Bootstrap/SASS', 'Heroku', 'HTML'], 'primary':'Ruby', 'display': True}, {'name':'frm','title': 'Farmstay (WIP)', 'link':'', 'created_at': datetime, 'image': '', 'body':'Build Advanced Rails App course from Ruby Thursday - Diving deeper into BDD, covering various stages from planning and stories, through permission scopes, and deploying stage and production.', 'tech': ['Ruby', 'Rails', 'ActiveRecord', 'Carrierwave/ImageMagick', 'BDD', 'Rspec w/ Capybara', 'Selenium Webdriver', 'Github', 'DigitalOcean', 'SSH, Apache'], 'primary':'Ruby', 'display': True}, {'name':'bng', 'title': 'Interrobang Man (Hangman)', 'link': 'https://sheltered-scrubland-38921.herokuapp.com/', 'created_at': datetime, 'image': 'http://arabianglimmer.com/images/intbng.png', 'body':'Build Advanced Rails App course from Ruby Thursday', 'tech': ['Ruby', 'Sinatra', 'Github', 'Heroku'], 'primary':'Ruby', 'display': True}, {'name':'rsa', 'title': 'Rowena Sandford Art', 'link': 'http://www.rowenasandfordart.com', 'created_at': datetime, 'image': 'http://arabianglimmer.com/images/rsa.png', 'body':"Built a custom artist's gallery using Wordpress, gallery plugin, CSS and HTML", 'tech': ['Wordpress', 'Various Plugins', 'Custom theme', 'CSS/HTML', 'Hosting'], 'primary':'Wordpress', 'display': True}, {'name':'bab', 'title': 'Birth and Bilinka', 'link': 'http://www.birthandbilinka.com', 'created_at': datetime, 'image': 'http://arabianglimmer.com/images/bb.png', 'body':'Built a website for a doula using Wordpress, gallery plugin, responsive theme, CSS and HTML', 'tech': ['Wordpress', 'Various Plugins', 'Responsive theme', 'CSS/HTML', 'Hosting'], 'primary':'Wordpress', 'display': True}, {'name':'cae','title': "Caesar's Cipher", 'link': 'https://pure-tundra-73618.herokuapp.com/', 'created_at': datetime, 'image': 'http://arabianglimmer.com/images/cc.png', 'body':"Caesar's Cipher built using Ruby and displaying through Sinatra framework.", 'tech': ['Ruby', 'Sinatra', 'Github', 'Heroku'], 'primary':'Ruby', 'display': True}]

def insert_portfolio_record(dictionary):
	folio = get_db(collection_name='portfolio')
	try:
		name = dictionary['name'] # unique identifier - not id number
		title = dictionary['title']
		link = dictionary['link']
		body = dictionary['body']
		image = dictionary['image']
		tech = dictionary['tech']
	except:
		return "Error - You're missing some required fields. Please review and submit again."

	insert_portfolio_data = {
			u'name': name,
			u'title': title,
			u'link': link,
			u'image': image,
			u'body': body,
			u'tech': tech,
			u'created': datetime.now()
	}

	msg = folio.insert_one(insert_portfolio_data)
	return "Success! Record added!"

for dictionary in my_list:
	msg = insert_portfolio_record(dictionary)
