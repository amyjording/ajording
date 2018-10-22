import os, os.path
import cherrypy
from view.app_core import *
from view.user_interface import *


def demo_template(content):
	header = header_template()
	navigation, navigation_row = navigation_template()
	
	html = f""" <!-- header -->
				{header}

		<!-- Dynamic svg text content here -->
				{navigation}
		<div class="container-fluid">
		  	<div class="wrapper">
								
				{navigation_row}

				<div class="row logorow">
					<div class="col"><h1>Try It</h1></div>
				</div>
				<div class="row">
					{content}
				</div>
		  	</div>
		</div>
		</body>
		</html>"""

	return html