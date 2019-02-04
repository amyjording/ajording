import os, os.path
import cherrypy
from view.app_core import *

def index_template():
	header = header_template()
	svg_text_template = " "
	circle_text = [{'id':'about', 'text':'About Me'},{'id':'work', 'text':'My Work'},{'id':'demo', 'text':'Try It'}, {'id':'contact', 'text':'Contact Me'}]
	for topic in circle_text:
		svg_text_template += """<svg style="display:none;">
								  <symbol id="{0}" viewBox="0 0 100 100">
									<circle cx="50" cy="50" r="50" />
									<text x="50%" y="50%" text-anchor="middle" fill="white" font-size="15px" font-family="Gruppo" dy=".3em" stroke-width="0">{1}</text>
									<path fill="currentColor"/>
								  </symbol>
								</svg>""".format(topic['id'], topic['text'])
	html = """ <!-- header -->
				{0}

		<!-- Dynamic svg text content here -->
		{1} <!-- <a id="shutdown"; href="./shutdown">Shutdown Server</a> -->

		<div class="container-fluid">
		  <div class="wrapper">
			<div class="row logorow">
			  <div class="col-sm-12 col-md-12 mainpagecol"><h1>Amy Jording</h1></div>
			</div>
			<div class="row mainpagerow">
			  <div class="col-xs-12 col-sm-3 col-md-3 mainpagecol"><a id="about-link" href="/about"><svg class="sass"><use xlink:href="#about" /></svg></a></div>
			  <div class="col-xs-12 col-sm-3 col-md-3 mainpagecol"><a id="work-link" href="/work"><svg class="sass sass--color"><use xlink:href="#work" /></svg></a></div>
			  <div class="col-xs-12 col-sm-3 col-md-3 mainpagecol"><a id="demo-link" href="/demo"><svg class="sass sass--invert"><use xlink:href="#demo" /></svg></a></div>
			  <div class="col-xs-12 col-sm-3 col-md-3 mainpagecol"><a id="contact-link" href="/contact"><svg class="sass sass--purple custom"><use xlink:href="#contact" /></svg></a></div>
			</div>
		  </div>
		</div>
		</body>
		</html>""".format(header, svg_text_template)

	return html


def aboutme_template():
	header = header_template()
	navigation, navigation_row = navigation_template()
	
	html = """ <!-- header -->
				{0}

		<!-- Dynamic svg text content here -->
				{1}
		<div class="container-fluid">
		  	<div class="wrapper">
								
				{2}

				<div class="row logorow">
					<div class="col"><h1>About Me</h1></div>
				</div>
				<div class="row">
					<div class="col about"><h4>In 1996, I took my first step with development. Thanks to Angelfire and Geocities, 
					I learned the magic of HTML, and can't begin to tell you how utterly baffled I was at the concept of 
					magically getting my picture from my computer out onto this page that was 'somewhere out there'. When I finally
					grasped the concept of uploading, it opened up a world of possibilities in my mind.</h4><h4>In 2001, I took an internship with a local media company. There,
					I applied my HTML and CSS knowledge on a few projects, and even became familiar with Adobe Premiere as well as
					Macromedia Flash Player. I got a taste of understanding layers and got my feet wet with "keys". It was a great
					learning experience over the course of 6 months.</h4>
					<h4>In 2004, I discovered Wordpress. It opened my eyes to 
					the concept of a template, and helped me to comprehend the idea of keeping data stored separately from
					the visual interface. While at the time, I still mostly used it for blogging, I enjoyed exploring the 
					nuts and bolts of how it worked. Eventually, I wound up buying my own hosting account in 2007, and consequently
					explored the nooks and crannies such as CPanel, phpMyAdmin, ftp, filemanager, etc.</h4></div>
				</div>
				<div class="row">
					<div class="col about"><h4>Throughout the span of the 2000s, I mainly worked in some form of supportive position. 
					From mastering Espresso (came in 5th at a Barista competition in Seattle back in 2000), to a temporary job at a banking 
					call center, from an assistant at a Diode Laser manufacturer, to another at an Aerospace parts distributer; from working on storage facility security 
					software maps with PaintShop Pro (2007), to Assistant Support Person for Kroger HQ (2008-2010), I've encompassed 
					quite a variety of "on the job" skills.</h4>
				</div>				
				</div>
				<div class="row">
					<div class="col about"><h4>In 2010, I started a blog called Arabian Glimmer. I have always been a big fan of
					the Arabian horse breed, and had a knack for remembering hundreds of horses and even memorizing pedigrees. So
					I decided to take this to a more public forum and follow my heart.</h4>
					<h4> By 2011, I wanted to gain a better understanding
					of website/user interface styling, and so I decided to basically reverse engineer an existing Wordpress template
					and make it my own, while learning different styling techniques.</h4>
					</div>
				</div>
				<div class="row">
					<div class="col about"><h4>From 2012 through 2017, I was essentially on a bit of a pre mid-life sabbatical. I 
					immersed myself in sustainable farm-life and the concept of Permaculture while doing an internship with a
					non-profit called World Steward, in the Columbia Gorge. I hauled hay, learned how to be a steward of the forest (Scotch broom is 
		            awful!), and grew a wide variety of crops. <br /><br />
		            Eventually, I came back to the regular working world for a short time and worked as seasonal Quality Assurance inspector
		            for a print production company, and not long after that, enjoyed three years in Ensenada, BC, Mexico.</h4>
		            </div>
		        </div>
				<div class="row">
					<div class="col about">        
					<h4>In 2016, I finally embraced the path of a Full Stack Web Developer. I rolled up my sleeves and began my self-taught
					 journey with <a href="https://www.theodinproject.com/">The Odin Project</a>. I took the long road and committed to understanding how to program with Ruby. What I was
					really doing was setting the foundation for what it takes to develop. Try, Fail, Research, Try again, Fail again
					(with great enthusiasm because the failure is new!), rinse and repeat until I would reach the finish line.</h4>
					<h4>Toward the end of 2016, I still wasn't completely finished with the Rails portion of
					The Odin Project, but I was actively looking for some sort of stepping stone toward being able to bring an income
					in and possibly keep learning. I found an opportunity and applied.</h4>
					<h4> After about three months of dead silence, I 
					was completely surprised with a response from a great Non-profit company, Keystone Accountability. 
					I started as a "Tech Fellow" (what I affectionately dub, a "Pre-Junior Developer"), and felt the sting of hot coals 
					on my digital feet as I faced my trial by fire, first into Python, Cherrypy, Drupal, Bootstraps, Ajax, and JavaScript. </h4>
					<h4>
					I learned a great deal about the Linux system through SSH (though I began most of my learning with Windows, so I had extra 
					hills to climb), learned the importance of staging and development, wrestled with version control with Github, and grew to
					have my own database preference (I adore MongoDB). I even wound up developing their user login system so that we could detach from Drupal, which was the user management portion of the site.</h4>
					<h4>After working for them for a year, they promoted me to Web Developer. All the while, I've been committed to continued learning
					and absolutely had to build this portfolio from scratch before I felt ready to reach out and find my (hopefully) permanent
					home for the rest of my career.<br /><br /></div>
				</div>
		  	</div>
		</div>
		</body>
		</html>""".format(header, navigation, navigation_row)

	return html

def contactme_template():
	header = header_template()
	navigation, navigation_row = navigation_template()
	
	html = f"""<!-- header -->
				{header}

		<!-- Dynamic svg text content here -->
				{navigation}
		<div class="container-fluid">
		  	<div class="wrapper">
								
				{navigation_row}

				<div class="row logorow">
					<div class="col"><h1>Contact Me</h1></div>
				</div>
				<div class="row">
					<div class="col"><h4>Linked In</h4><h4>Twitter</h4><h4>Github</h4></div>
					<div class="col"></div>
				</div>
				<div class="row">
					<div class="col"><h4>Email Contact Form</h4></div>				
				</div>
				<div class="row">
					<div class="col"><h4></h4></div>
					<div class="col"><h4></h4></div>
				</div>
				<div class="row">
					<div class="col"><h4></h4></div>				
				</div>
		  	</div>
		</div>
		</body></html>"""
	return html