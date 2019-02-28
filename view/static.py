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
			  <div class="col-xs-12 col-sm-3 col-md-3 mainpagecol label-bold"><a id="about-link" href="/about"><svg class="sass"><use xlink:href="#about" /></svg></a></div>
			  <div class="col-xs-12 col-sm-3 col-md-3 mainpagecol label-bold"><a id="work-link" href="/work"><svg class="sass sass--color"><use xlink:href="#work" /></svg></a></div>
			  <div class="col-xs-12 col-sm-3 col-md-3 mainpagecol label-bold"><a id="demo-link" href="/demo"><svg class="sass sass--invert"><use xlink:href="#demo" /></svg></a></div>
			  <div class="col-xs-12 col-sm-3 col-md-3 mainpagecol label-bold"><a id="contact-link" href="/contact"><svg class="sass sass--purple custom"><use xlink:href="#contact" /></svg></a></div>
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
					<div class="col-xs-12 col-sm-6 col-md-6 about label-bold">
					<table class="characterTable">
						<thead>
							<tr>
								<th colspan="2"><h2>Character Stats</h2></th>
							</tr>
						</thead>
						<tfoot>
							<tr>
								<td colspan="2">
								<div class="centered"><h2>Backstory</h2></div>
								</td>
							</tr>
						</tfoot>
						<tbody>
							<tr>
								<td>Species:</td>
								<td>Female Human</td>
							</tr>
							<tr>
								<td>Class:</td>
								<td>Technically, a Developer</td>
							</tr>
							<tr>
								<td>Languages:</td>
								<td>Python, Ruby, Javascript (jQuery, ajax, D3), HTML/CSS</td>
							</tr>
							<tr>
								<td>Frameworks:</td>
								<td>Cherrypy, Ruby on Rails</td>
							</tr>
							<tr>
								<td>Databases:</td>
								<td>MongoDB, MySQL, Postgresql</td>
							</tr>
							<tr>
								<td>Management:</td>
								<td>Github, Trello, Slack</td>
							</tr>
							<tr>
								<td>People Skills:</td>
								<td>Patient, Supportive, Flexible</td>
							</tr>
							<tr>
								<td>Skillz:</td>
								<td>Listening, Working with scraps, adapting, writing</td>
							</tr>
							<tr>
								<td>Mood:</td>
								<td>Upbeat and positive, with a touch of muse</td>
							</tr>
							<tr>
								<td>Motto:</td>
								<td>"There has to be a mod for this."</td>
							</tr>
						</tbody>
					</table>
					</div>
					<div class="col-xs-12 col-sm-6 col-md-6 about">
						<div class="trading-card">
							<h4 class="label-bold" style="background-color: #f1f1f1;">Amy G Dala &nbsp;&nbsp;&nbsp; <span style="color: red;">HP 120</span></h4>
							<img style="width: 100%; max-width: 350px; border: 2px solid black; margin: 0 auto 8px auto; display: block;" src="https://lh3.googleusercontent.com/YBheu72xdgoEFc0yHJoGmVOHAeMcjkoDeXkhZZhe1PtduTKcx98hJb0UQOmimnfeovTBSlXXzhkBPFdoaPrsCmYZp7tygPQ7dX77onVldWyHDHS3WAAIFywOk_ZdWflMjv8WTUqpTgq8VhRKdmpxU2vnhUbD28DasrbyKkVWPTmqxWB-CEapBcyaCSzyK5den1LbMyWD2GwSGvJBcZmn6zbYIh8yU4fAhPQaqQV3Q72y7nkeDKW4dki3jwpyhVG8szzQu7CQlZh_Q_LYqI_gQrGm6-GjJ6tpZOvkNJdHzOx1_RUcgE1Pxu8-0QWuBMrLcE0HimjoNJl5TkL4xvzIKh362vRexc3UFKxZLl27-gyoHcTEM3Z40XN9UlmQzML_mjN6kmt1pAwkwRPoTEXkONRGYNQyFqsqX41iXHGexwEdP0clWbNlg7H9nvojnM2YRYzws6h7yFwvaX-sRPoa7ZBaABC6JquZ-44ix797WuWmdu63ehXcaI-nDwq-ZPrHyZa9P7e2rkkOYtlVg58w9FfLAOH1N-f_H0w2-l4tGqVahSTPm6MoIFw5zeuW4_72UaauAAH1-U7FqFm-djuOG70ZpjP6SG0AHxrr2R4CUfis4z0YWBst11-A7CwyOj7K2V07xCYfmtjfAUTs9I341PQnmNM-l2o=w1080-h1081-no">
							<div style="background-color: #f1f1f1;">
								<h5 class="label-bold" style="margin-left: -15px;"> Weapon: Laser cats </h5>
								<h5 class="label-bold" style="margin-left: -15px;"> Specialty: W A S D </h5>
								<h6 class="label-bold" style="padding-right: 3px; margin-left: -10px;">weakness: overthinks | resistance: small talk</h5>
								<hr>
								<h6 class="label-bold" style="margin-left: -15px; padding-bottom: 4px;"> Willing to tackle most anyhing. Runs 300+ mods in Skyrim. </h5>
							</div>
						</div>
					</div>
				</div>
				<div class="row">
					<div class="col about"><br />
					<h4>In 1996 (uh, yeah, I'm getting up there), fresh out of high school, I took my first step with development. Thanks to Angelfire and Geocities, 
					I learned HTML. I still remember how baffled I was by the concept of "magically" 
					getting my picture from my computer out onto this page that was 'somewhere out there'. That's when I grasped the 
					concept of uploading and it opened up a curiosity into the world of digital possibilities.</h4>

					<h4>Later on, I interned with a local media company and got familiar with using Adobe Photoshop, Adobe Premiere, and Macromedia 
					Flash Player (that should date me); tools that taught me how to use layers, and so much more.</h4>
					</div>
				</div>
				<div class="row">
					<div class="col about">
					<h4>I worked in supportive roles in interesting and diverse places. From my span of experiences, I mastered Espresso (came in 5th at a Seattle Barista competition),
					learned a lot of people skills, general office protocal, but I also learned cool skills like how to buy aerospace parts and how to turn AutoCAD drawings into interactive digital
					maps for custom security system software.
					</h4>
					</div>				
				</div>
				<div class="row">
					<div class="col about">
					<h4>Then Wordpress came along, and I got well acquainted with it as I blogged about Arabian horses. It helped me comprehend the idea of templates and keeping data stored separately from
					the visual interface. I got a sense that this technology could be a lot more than just a blog. I explored around the backend a bit,
					and started learning about the power of dynamic content. Eventually, I also got familiar with hosting interfaces and tools such as CPanel, phpMyAdmin, ftp, filemanager, etc.
					</h4>
					</div>
				</div>
				<div class="row">
					<div class="col about">
					<h4>I was afforded the chance to immerse myself in sustainable farm-life and committed to an internship with a non-profit 
					organization called World Steward, in the Columbia Gorge (Oregon/Washington). 

					I hauled hay, learned how to be a steward of the forest 
					(I hate Scotch broom), and grew a wide variety of crops. I also fell in love with <a href="https://en.wikipedia.org/wiki/Permaculture">
					Permaculture</a>.</h4>
		            </div>
		        </div>
				<div class="row">
					<div class="col about">        
					<h4>In 2016, I finally embraced the path of a Full Stack Web Developer. I rolled up my sleeves and began my self-taught
					 journey with <a href="https://www.theodinproject.com/">The Odin Project</a>. Through the course, I was setting the foundation 
					 for what it takes to develop: Try, Fail, Research, Try again, Fail again (with great enthusiasm because the failure is new!), rinse and repeat until I 
					 would reach the finish line.</h4>

					<h4>In early 2017, I found an amazing opportunity to both learn and work remotely for the non-profit organization, Keystone 
					Accountability. I began my developing journey working remotely as a "Tech Fellow", and felt the sting of hot coals on my digital feet as I faced my trial-by-fire into Python, Cherrypy, Drupal, Bootstrap, Ajax, and JavaScript. 
					I got used to feeling stupid a lot.</h4>
					
					<h4>Through my time with them, I've also learned a great deal about the Linux system through SSH (though I began most of my learning with Windows, so I had extra 
					hills to climb), learned the importance of staging and development, wrestled with version control with Github, and grew to
					have my own database preference (I adore MongoDB). I even wound up developing their user login system from scratch so that 
					the site could completely detach from using Drupal.</h4>

					<h4>After working for them for a year, they promoted me to Developer, and I feel ready to level up and 
					find my permanent home as a Full Stack Web Developer!</h4><br /><br /></div>
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