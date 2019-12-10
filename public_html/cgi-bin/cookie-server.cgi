#!/usr/bin/env python

import sys
import Cookie
import datetime
import random
import cgi
import cgitb; cgitb.enable()  # for troubleshooting

sys.stderr = sys.stdout

expiration = datetime.datetime.now() + datetime.timedelta(days=30)
cookie = Cookie.SimpleCookie()
cookie["session"] = 2
#cookie["session"]["domain"] = ".jayconrod.com"
#cookie["session"]["path"] = "/"
#cookie["session"]["expires"] =  expiration.strftime("%a, %d-%b-%Y %H:%M:%S PST")



######## Dynamic HTML Page
print "Content-type: text/html"
print

print """
<html>

<head><title>CGI Cookie Server</title></head>

<body>

  <h3> All the cookies your browser sending:</h3>
"""

form = cgi.FieldStorage()
message = form.getvalue("message", "(no message)")

print """

  <p>Previous message: %s</p>

  <p>form

  <form method="post" action="index.cgi">
    <p>message: <input type="text" name="message"/></p>
  </form>

</body>

</html>
""" % cgi.escape(message)
