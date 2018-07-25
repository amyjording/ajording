import os, os.path
import cherrypy
from view.app_core import *

def work_template():
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
					<div class="col"><h1>My Work</h1></div>
				</div>
				<div class="row">
					<div class="col"><p>Placeholder for my portfolio</p></div>
					<div class="col"></div>
				</div>
				<div class="row">
					<div class="col"><p></p></div>				
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
		</body>
		</html>""".format(header, navigation, navigation_row)

	return html