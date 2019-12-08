#!/usr/bin/python

import socket
import time
import sys
#import base64, getpass, ssl

sys.stderr = sys.stdout

# Import modules for CGI handling
import cgi, cgitb
cgitb.enable()

def send_recv(socket, msg, code):
    if msg != None:
        print "Sending==> ", msg
        socket.send(msg + '\r\n')

    recv = socket.recv(1024)
    print "<==Received:\n", recv
    if recv[:3]!=code:
        print '%s reply not received from server.' % code
    return recv

def send(socket, msg):
    print "Sending ==> ", msg
    socket.send(msg + '\r\n')



# Create instance of FieldStorage
form = cgi.FieldStorage()

# Get data from fields
fromAddress = form.getvalue('from')
#emailServerName = fromAddress.split("@").partition(".")[1]
to  = form.getvalue('to')
subject = form.getvalue('subject')
message = form.getvalue('message')




# Debug and logging
print fromAddress, to, subject, message


serverName = 'smtp.cis.fiu.edu'
serverPort = 25

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
recv=send_recv(clientSocket, None, '220')

clientName = 'Example-kianmrf-CNT4713'
#userName="kmtestpy"
userName = fromAddress.split('@')[0]
userServer= fromAddress.split('@')[1]
toName= to.split('@')[0]
toServer= to.split('@')[1]
#Send HELO command and print server response.
heloCommand='EHLO %s' % clientName
recvFrom = send_recv(clientSocket, heloCommand, '250')
#Send MAIL FROM command and print server response.
fromCommand='MAIL FROM: <%s@%s>' % (userName, userServer)
recvFrom = send_recv(clientSocket, fromCommand, '250')
#Send RCPT TO command and print server response.
rcptCommand='RCPT TO: <%s@%s>' % (toName, toServer)
recvRcpt = send_recv(clientSocket, rcptCommand, '250')
#Send DATA command and print server response.
dataCommand='DATA'
dataRcpt = send_recv(clientSocket, dataCommand, '354')
#Send message data.
send(clientSocket, "Date: %s" % time.strftime("%a, %d %b %Y %H:%M:%S -0400", time.localtime()));
send(clientSocket, "From: <%s@%s>" % (userName, userServer));
send(clientSocket, "Subject: %s" % (subject));
send(clientSocket, "To: %s@%s" % (toName, toServer));
send(clientSocket, ""); #End of headers
send(clientSocket, message);
#send(clientSocket, "Hola Mundo");
#send(clientSocket, "ocelot client");
#Message ends with a single period.
send_recv(clientSocket, ".", '250');
#Send QUIT command and get server response.
quitCommand='QUIT'
quitRcpt = send_recv(clientSocket, quitCommand, '221')

print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<title>E-mail Client Example</title>"
print "</head>"
print "<body>"
#print "<script>"
#print "    alert('%s')" % (emailServerName)
#print "</script>"
print "<h1>E-mail Client Example</h1>"
print "<form action='/~mmaro017/cgi-bin/send-email.cgi' target='_self' method='get' >"
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
print "<input type='submit' value='Send Again!'>"
print "</fieldset>"
print "</form>"
# print "<h2>Hello %s %s %s %s</h2>" % (fromAddress.split('@')[0], to.split('@')[1], subject, message)
print "</body>"
print "</html>"
