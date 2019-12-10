#!/usr/bin/env python

import os
import Cookie

print "Content-type: text/html\n\n"

print """
<html>
<body>
<h1>Check the cookie</h1>
"""

if 'HTTP_COOKIE' in os.environ:
    cookie_string=os.environ.get('HTTP_COOKIE')
    c=Cookie.SimpleCookie()
    c.load(cookie_string)

    try:	
        for ckey in c.keys():
		data = c[ckey].value
		print "cookie name: " + ckey + "   "
		print "cookie data: " + data + "<br>" 
        #data=c['LPVID'].value
        #print "cookie data: "+data+"<br>"
    except KeyError:
        print "The cookie was not set or has expired<br>"


print """
</body>
</html>

"""
