#!/usr/bin/python

import base64, getpass, socket, ssl, sys
# Import modules for CGI handling
import cgi, cgitb

sys.stderr = sys.stdout
cgitb.enable()

form = cgi.FieldStorage()
fromAddress = form.getvalue('from')
to  = form.getvalue('to')
subject = form.getvalue('subject')
message = form.getvalue('message')


print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<title>E-mail Client Example</title>"
print "</head>"
print "<body>"
print "<h1>E-mail Client Example -- GMail Auth. Only!</h1>"
print "<form action='/~mmaro017/cgi-bin/new-email.cgi' target='_self' method='get' >"
print "<fieldset>"
print "<legend>Email Contents:</legend>"
print "From address:<br>"
print "<input type='text' name='from' value='%s'><br>" % (fromAddress)
print "To address:<br>"
print "<input type='text' name='to' value='%s'><br>" % (to)
print "Subject:<br>"
print "<input type='text' name='subject' value='%s'><br>" % (subject)
print "Message:<br>"
print "<input type='text' rows='6' cols='50' name='message' value='%s'></textarea><br><br>" % (message)
# print "<input type='submit' value='Send Again!'>"
print "</fieldset>"
#print "</form>"
#print "<form>"
print "<fieldset>"
print "<legend>Authenticate with your credentials:</legend>"
print "Username:<br>"
print "<input type='text' name='username' value=''><br>"
print "Password:<br>"
print "<input type='text' name='password' value=''><br>"     
print "<input type='submit' value='Authenticate with GMAIL and Send message'>"
print "</fieldset>"
print "</form>"
# print "<h2>Hello %s %s %s %s</h2>" % (fromAddress.split('@')[0], to.split('@')[1], subject, message)
print "</body>"
print "</html>"



def test():
#   testff = "test@gmail.com"
#    print(testff.split("@").partition("."))
    print("Test")
    

test1 = "test@gmail.com"
#print "%s" %(test1)

emailServerName = fromAddress.split("@")[1]
print(emailServerName)

#if "google.com" in emailServerName:
#   mailserv = "smtp.gmail.com"
#   mailport = 465
#   print("kir")
#elif emailServerName=="yahoo.com":
#   mailserv = "smtp.mail.yahoo.com"
#   mailport = 465
#elif emailServerName=="fiu.edu":
#    mailserv = "smtp.cis.fiu.edu"
#    mailport = 25
#else:
#    print("Mail Server Authentication is not yet supported for the senders email provider")


#if "google" in fromAddress:
#    mailserv = 'smtp.gmail.com
#    mailport = 465
#if "yahoo" in fromAddress:
#    mailserv = 'smtp.mail.yahoo.com'
#    mailport = 465
#if "fiu" in fromAddress:
#    mailserv = 'smtp.cis.fiu.edu'
#    #print "<h1 style="color=red"> ERROR: This mail server is not supported yet! </h1>"

mailserv = 'smtp.gmail.com'
mailport = 465

username = form.getvalue('username')
password = form.getvalue('password')

def getSSLSocket():
    return ssl.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), ssl_version=ssl.PROTOCOL_SSLv23)


def main():
# Get the socket
#    if cryptmethod == 'SSL':
#        sock = getSSLSocket()
#    elif cryptmethod == 'TLS':
#        sock = getTLSSocket()
#    else:
#        sock = getPlainSocket()
    sock = getSSLSocket()
    # Attempt to connect to the SMTP server
    sock.connect((mailserv, mailport))
    # Receive response from server and print it
    respon = sock.recv(2048)
    # print(str(respon, 'utf-8'))
    # Say HELO and print response
    heloMesg = 'HELO Derpy\r\n'
    # print(heloMesg)
    sock.send(heloMesg.encode('utf-8'))
    respon = sock.recv(2048)
    # print(str(respon, 'utf-8'))
    # Authenticate with the server
    authMesg = 'AUTH LOGIN\r\n'
    crlfMesg = '\r\n'
    # print(authMesg)
    sock.send(authMesg.encode('utf-8'))
    respon = sock.recv(2048)
    # print(str(respon, 'utf-8'))
    user64 = base64.b64encode(username.encode('utf-8'))
    pass64 = base64.b64encode(password.encode('utf-8'))
    # print(user64)
    sock.send(user64)
    sock.send(crlfMesg.encode('utf-8'))
    respon = sock.recv(2048)
    # print(str(respon, 'utf-8'))
    # print(pass64)
    sock.send(pass64)
    sock.send(crlfMesg.encode('utf-8'))
    respon = sock.recv(2048)
    # print(str(respon, 'utf-8'))
    # Tell server the message's sender
    fromMesg = 'MAIL FROM: <' + fromAddress + '>\r\n'
    # print(fromMesg)
    sock.send(fromMesg.encode('utf-8'))
    respon = sock.recv(2048)
    # print(str(respon, 'utf-8'))
    # Tell server the message's recipient
    rcptMesg = 'RCPT TO: <' + to + '>\r\n'
    # print(rcptMesg)
    sock.send(rcptMesg.encode('utf-8'))
    respon = sock.recv(2048)
    # print(str(respon, 'utf-8'))
    # Give server the message
    dataMesg = 'DATA\r\n'
    # print(dataMesg)
    sock.send(dataMesg.encode('utf-8'))
    respon = sock.recv(2048)
    # print(str(respon, 'utf-8'))
    mailbody = message + '\r\n'
    # print(mailbody)
    sock.send(mailbody.encode('utf-8'))
    fullStop = '\r\n.\r\n'
    # print(fullStop)
    sock.send(fullStop.encode('utf-8'))
    respon = sock.recv(2048)
    # print(str(respon, 'utf-8'))
    # Signal the server to quit
    quitMesg = 'QUIT\r\n'
    # print(quitMesg)
    sock.send(quitMesg.encode('utf-8'))
    respon = sock.recv(2048)
    # print(str(respon, 'utf-8'))
    # Close the socket to finish
    sock.close()



main()
