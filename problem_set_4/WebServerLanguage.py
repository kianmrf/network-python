from socket import socket, SOCK_STREAM, AF_INET
import webbrowser
#Create a TCP socket
#Notice the use of SOCK_STREAM for TCP packets


def openTcpSocket(serverPort):
    socket1 = socket(AF_INET, SOCK_STREAM)
    # Assign IP address and port number to socket
    socket1.bind(('', serverPort))
    socket1.listen(1)
    print ("Interrupt with CTRL-C")
    return socket1

def main():
    serverSocket = openTcpSocket(1616)
    buf = ""
    key = None
    modified = None
    while True:
        try:
            # establish the connection
            print "Ready to serve..."
            connectionSocket, addr = serverSocket.accept()
            # readHeaders need to be defined
            headers, post_data = readHeaders(connectionSocket)
            filename = headers["STATUS-LINE"].split()[1].partition("/")[2]
            print "Status Line: " , headers["STATUS-LINE"]
            filenameLanguage = acceptLanguageModifyFile(filename, headers)
            seconds = None
            if filenameLanguage == filename:
                seconds = ifModifiedSinceSeconds(headers)
            sendFile(connectionSocket, filenameLanguage, "text/plain", seconds)
            connectionSocket.shutdown(SHUT_WR)
            connectionSocket.close()
        except IOError:
            print "Not found %s" % filename
            sendError(connectionSocket, '404','Not Found')
            connectionSocket.shutdown(SHUT_WR)
            connectionSocket.close()
        except KeyboardInterrupt:
            print "\n Interrupted by CTRL-C"
            break
    serverSocket.close()

main()

