#!/usr/bin/python

import os
import sys
import mod_html

sys.stderr = sys.stdout

def html(value):
	# load page
	print """\
		<!doctype html>
		<html>
			<head>
				<title> FTP Proxy Example </title>
			</head>
			<body>
				<h1> Welcome to FTP Client </h1>
				<p>
					Enter Filename: <input type="text" name="filename" value=""></input>				
				
					<input type="submit" value="Submit" >
				</p>
				
			</body>
		</html>""".format(value)
def main():
	print "Content-type: text/html\n";
	value = ""
	parsed = mod_html.parse()
	if 'filename' in parsed:
		value = parsed['filename']
	html(value)
	
main()
