#!/usr/bin/env python

import sys
import Cookie
import datetime
import random
import cgi
import cgitb; cgitb.enable()  # for troubleshooting

sys.stderr = sys.stdout

#expiration = datetime.datetime.now() + datetime.timedelta(days=30)
#cookie = Cookie.SimpleCookie()
#cookie["session"] = random.randint(1, 100000)
#cookie["session"]["domain"] = "ocelot.aul.fiu.edu"
#cookie["session"]["path"] = "/mmaro017/cgi-bin/cookie-server.cgi"
#cookie["session"]["expires"] =  expiration.strftime("%a, %d-%b-%Y %H:%M:%S PST")



######## Dynamic HTML Page
print "Content-type: text/html"
#print(cookie.output())
print

print """
<html>

<head><title>CGI Cookie Server</title></head>

<body>

  <h3> All the cookies your browser sending:</h3>
"""

form = cgi.FieldStorage()
message = form.getvalue("message", "(no message)")

#print(cookie.output())

print """

  <p>Previous message: %s</p>

  <p>

  <form method="post" action="cookie-server.cgi">
    <p>message: <input type="text" name="message"/></p>
  </form>

</body>

</html>
""" % cgi.escape(message)
