#FTPClient.py

from socket import socket, AF_INET, SOCK_STREAM
from ast import literal_eval
import time
import sys

def send(socket, msg): 
	print "===>sending: " + msg
	socket.send(msg + "\r\n")
	recv = socket.recv(1024)
	print "<===receive: " + recv
	return recv
	
serverName = 'ftp.swfwmd.state.fl.us'
serverPort = 21
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
condition = True
message = clientSocket.recv(2048)
print message
while condition:
	message = clientSocket.recv(2048)
	print message
	condition = message[0:6] != "220---"
message = send(clientSocket,"USER Anonymous")
message = send(clientSocket,"PASS kianmrf@cs.fiu.edu")
message = send(clientSocket,"TYPE A")
message = send(clientSocket,"PASV")
start = message.find("(")
end  = message.find(")")
tuple = message[start+1:end].split(',')
print tuple
#build the port from the last two numbers
port = int(tuple[4])*256 + int(tuple[5])
print port
dataSocket = socket(AF_INET, SOCK_STREAM)
dataSocket.connect((serverName, port))
message = send(clientSocket,"LIST")
message = dataSocket.recv(2048)
print message
message = clientSocket.recv(2048)
print message
dataSocket.close()
message = send(clientSocket,"QUIT")
clientSocket.close()
