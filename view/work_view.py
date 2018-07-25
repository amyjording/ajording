import os, os.path
import cherrypy
from view.app_core import *
from controllers.portfolios import *

def work_template():
	header = header_template()
	navigation, navigation_row = navigation_template()
	portfolio_content = u""" """
	portfolios = get_portfolios()
	for portfolio in portfolios:
		tech = '•'
		for lang in portfolio['tech']:
			tech += ' {0} •'.format(lang)
		portfolio_content += u"""<div class="col-lg-8 col-md-8 mx-auto col-sm-12 col-xs-12 folio">
		<header>
          <h2 class='text-center'>{0}</h2>
          <blockquote class='text-center'><h4><b><a href="{1}">Visit URL</a></b></h4>
          </blockquote>
        </header>
        <img class='center-block img-thumbnail' src='{2}' alt='Image for {0}'>
        	<p></p>
        	<h3><b>What I developed</b></h3>
        	<h5>{3}</h5><br />
        	<h3><b>Technology</b></h3>
        	<h5 style="text-align: center;">{4}</h5> 
			<footer class="link text-center">
			</footer>
        </div>""".format(portfolio['title'], portfolio['link'], portfolio['image'], portfolio['body'], tech)
	
	html = """ <!-- header -->
				{0}

		<!-- Dynamic svg text content here -->
				{1}
		<div class="container-fluid">
		  	<div class="wrapper">
								
				{2}

				<div class="row logorow">
					<div class="col"><h1>My Work</h1></div>
				</div>
				<div class="row">
					{3}
				</div>			
		  	</div>
		</div>
		</body>
		</html>""".format(header, navigation, navigation_row, portfolio_content)

	return html