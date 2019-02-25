import os, os.path
import cherrypy

def header_template():
	template = """<!DOCTYPE html>
				<html lang="en">
				<head>
					<title>Amy Jording</title>
					<meta charset="utf-8" />
					<meta name="viewport" content="width=device-width, initial-scale=1">
					<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.1.0/css/bootstrap.min.css">
					<link href="/static/css/custom.css" rel="stylesheet">
					<link href="https://fonts.googleapis.com/css?family=Gruppo|Nixie+One" rel="stylesheet">
					<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
					<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.0/umd/popper.min.js"></script>
					<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.1.0/js/bootstrap.min.js"></script>
					<script src="/static/js/ajax.js"></script>
					<script src="/static/js/join.js"></script>
					<script src="/static/js/deleteaccount.js"></script>
				</head>
				<body>"""
	return template

def navigation_template():
	svg_nav_template = " "
	page_list = ['about', 'work', 'demo', 'contact']
	for page in page_list:
		if page in cherrypy.url():
			svg_nav_template += """<svg style="display:none;">
		 			<symbol id="{0}" viewBox="0 0 100 100">
						<circle cx="50" cy="50" r="50" fill-opacity="0.5" />
						<path fill="currentColor"/>
		  			</symbol>
				</svg>""".format(page)
		svg_nav_template +=  """<svg style="display:none;">
		 			<symbol id="{0}" viewBox="0 0 100 100">
						<a id="{0}-link" href="/{0}"><circle cx="50" cy="50" r="50" /></a>
						<path fill="currentColor"/>
		  			</symbol>
				</svg>""".format(page)
	nav_row = """<div class="row navheadrow">
			  		<div class="col-sm-12 col-md-12">
			  			<h2><a id="home" href="/">Amy Jording</a></h2>
			  		</div>
				</div>
				<div class="row navrow">
			  		<div class="col-md-12">
			  			<div class="row colwrapper">
			  				<div class="col-xs-12 col-sm-3 col-md-3 navcol"><svg class="sasssmall"><use xlink:href="#about" /></svg></div>
			  				<div class="col-xs-12 col-sm-3 col-md-3 navcol"><svg class="sasssmall sass--color"><use xlink:href="#work" /></svg></div>
			  				<div class="col-xs-12 col-sm-3 col-md-3 navcol"><svg class="sasssmall sass--invert"><use xlink:href="#demo" /></svg></div>
			  				<div class="col-xs-12 col-sm-3 col-md-3 navcol"><svg class="sasssmall sass--purple custom"><use xlink:href="#contact" /></svg></div>
						</div>
			  		</div>
				</div>"""
	return svg_nav_template, nav_row