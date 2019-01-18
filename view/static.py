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
		{1} <a id="shutdown"; href="./shutdown">Shutdown Server</a>

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
					<div class="col"><p>Back in 1997, I took my first step with development. Thanks to Angelfire and Geocities, 
					I learned the magic of HTML, and can't begin to tell you how utterly baffled I was at the concept of 
					magically getting my picture from my computer out onto this page that wasn't living on my computer. "Upload",
					I would later understand it to be.</p></div>
					<div class="col"><p>In 2004, I got acquainted with Wordpress. It was a blogging platform, but it didn't
					take long for me to see that a 'blog' and a 'page', were more or less, just labels and that one was a
					static behavior, while the other was dynamic. I didn't know those terms yet, but I had a feeling the sheer
					simplicity of how it was built, was a handy tool.</p></div>
				</div>
				<div class="row">
					<div class="col"><p>Throughout the years, on a professional scale, I mainly stuck to office support jobs. 
					I wanted to take my web knowledge further, but I really hadn't heard of many of the terms other than php,
					and to be honest, it was a nightmare code to try to dissassemble.</p><p> I did, however, get better
					acquainted with Adobe Create Suite, and got up to speed on the new concept of Responsive Design.</p> 
					<p>Life went on for a while, and I decided
					to volunteer on a farm for a Non-Profit in the Columbia Gorge area. I discovered a deep love for going 
					beyond the label of "sustainable", but pushed myself further into bountifully abundant due to a concept
					called permaculture.</p></div>				
				</div>
				<div class="row">
					<div class="col"><p>It's a passion that I plan on delving into for many years going forward. But I knew
					that the first step toward this bountiful sustaining lifestyle started with me. So I rolled up my sleeves 
					and committed to learning how to really develop. I got started with The Odin Project in 2016, and didn't 
					speed ahead to the Rails chapter. I made myself push through the hardest parts of Ruby (like building a chess game).</p></div>
					<div class="col"><p>In 2017, I caught a break with a great Non-profit company called Keystone Accountability. 
					I started as a "Tech Fellow" (what I lovely dub, a "Pre-Junior Developer"), and felt the sting of hot coals 
					on my digital feet as I dove head into Python, Cherrypy and Drupal. I even wound up developing their user 
					login system so that we could detach Drupal, which was the user management portion of the site.</p></div>
				</div>
				<div class="row">
					<div class="col"><p>I've had a unique experience in that I've learned the convention and convenience of Rails,
					but have come to really find more 'fun' from developing in pure Python using a minimalist framework like Cherrypy.
					</p></div>				
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
					<div class="col"><p>Linked In</p><p>Twitter</p><p>Github</p></div>
					<div class="col"></div>
				</div>
				<div class="row">
					<div class="col"><p>Email Contact Form</p></div>				
				</div>
				<div class="row">
					<div class="col"><p></p></div>
					<div class="col"><p></p></div>
				</div>
				<div class="row">
					<div class="col"><p></p></div>				
				</div>
		  	</div>
		</div>
		</body></html>"""
	return html