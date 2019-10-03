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
        filename = message.split()[1]
        # sendFile(connectionSocket, filename, 'text/plain')
        f = open(filename[1:])
        print("KIR TYPE: "+filename[2:])
        outputdata = f.read()
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i])
        print("Success! File sent!")
            # Capitalize the message from the client
        # message = message.upper()
        # connectionSocket.send(message.encode())
        connectionSocket.close()
    except IOError:
        errormsg = 'File Not Found - 404'
        print(errormsg)
        connectionSocket.send(errormsg).encode()
        # endError(connectionSocket, '404', 'Not found')
        connectionSocket.close()
    except KeyboardInterrupt:
        print ("\nInterrupted by CTRL-C")
        break


serverSocket.close()

