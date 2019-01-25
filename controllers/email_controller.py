import sendgrid
import requests
import cherrypy
import os
from sendgrid.helpers.mail import *
from config.secrets import secrets



def send_mail(to_email, subject, message):

	#example:
	#data = {"personalizations":[{"to":[{"email":"zanizm@gmail.com"}],"subject":"I'm sending this to you from my Ubuntu Terminal."}],"from":{"email":"zanizm@gmail.com"},"content":[{"type":"text/plain", "value":"Hiya! I just sent this from my computer terminal. Testing out the email app I'm going to use for the portfolio. Toodloo! Gmail might freak out but I promise it's fine and has no spam."}]}
	secret = secrets()
	sg = sendgrid.SendGridAPIClient(apikey=secret['SENDGRID_API_KEY'])
	data = {"personalizations":[{"to":[{"email":to_email}],"subject":subject}],"from":{"email":"noreply@amyjording.com"},"content":[{"type":"text/plain", "value":message}]}
	response = sg.client.mail.send.post(request_body=data)
	return response.status_code