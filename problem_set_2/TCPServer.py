#TCPServer.py

from socket import socket, SOCK_STREAM, AF_INET
#Create a TCP socket 
#Notice the use of SOCK_STREAM for TCP packets
serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort=1616
# Assign IP address and port number to socket
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print ("Interrupt with CTRL-C")
while True:
	try:
            connectionSocket, addr = serverSocket.accept()
            print ("Connection from %s port %s" % addr)
		# Receive the client packet
            message = connectionSocket.recv(4096).decode()
            print ("Orignal message from client: ", message)
		# Send file requested
	    filename = message.split().partition("/")
	    sendFile(connectionSocket, filename, 'text/plain')

		# Capitalize the message from the client
            # message = message.upper()
            # connectionSocket.send(message.encode())
            connectionSocket.close()
	except KeyboardInterrupt:
            print ("\nInterrupted by CTRL-C")
            break
	except IOError:
	    print("Not foun %s" % filename)
	    sendError(connectionSocket, '404', 'Not found')
	    connectionSocket.close()

serverSocket.close()
