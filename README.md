# Amy Jording - Portfolio

Amy's Portfolio App created from scratch with Python and Cherrypy. See the portfolio in action at: [https://www.amyjording.com](https://www.amyjording.com/) 

## To Test Locally:

Fork and clone. See the requirements for modules in the next section.
MongoDB 4.0 required for data storage.
SendGrid for sending Activation and Reminder tokens.

The Daily API refreshes via a script that runs once a day through a cron trigger.
The script is (script name here), and can be manually called on a local test to 
check that it refreshes properly.


### Modules used

Python Modules - Pip install the following:

```
Cherrypy     - v 18.1.0 - Framework
Pymongo      - v 3.7.2  - Database
Bcrypt       - v 3.1.6  - Encryption
itsdangerous - v 1.1.0  - Serializing
jinja2       - v 2.10   - Templates
bs4          - v 0.0.1  - Webscraping
wikia        - v 1.4.3  - Wikia wrapper
SendGrid     - v 5.6.0  - Email Dispatch

```

## Built With

* [Cherrypy](https://cherrypy.org/) - The web framework used
* [MongoDB](https://www.mongodb.com/) - The database
* [Jinja2](http://jinja.pocoo.org/) - Templates


## Authors

* **Amy Jording**


## Acknowledgments

* Login & Signup credits: Claudia Romano [CodyHouse](https://codyhouse.co/) & [Emil](https://codepen.io/emilcarlsson/pen/XbZprZ)

