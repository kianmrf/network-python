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

def header2dict(data):
    data = data.replace("\n ", " ").splitlines()
    headers = {}
    for line in data:
        split_here = line.find(":")
        headers[line[:split_here]] = line[split_here:]
    return headers

def parseAcceptLanguage(acceptLanguage):
    languages = acceptLanguage.split(",")
    locale_q_pairs = []

    for language in languages:
        if language.split(";")[0] == language:
          # no q => q = 1
          locale_q_pairs.append((language.strip(), "1"))
        else:
          locale = language.split(";")[0].strip()
          q = language.split(";")[1].split("=")[1]
          locale_q_pairs.append((locale, q))

    return locale_q_pairs

def acceptLanguageModifyFile(filename, headers):
    acceptedLanguages = parseAcceptLanguage(headers["Accept-Language"])
    # preferredLanguage is the first language in the list
    preferredLanguage =  acceptedLanguages[0][0].replace(': ', '')
    if preferredLanguage == "en-us":
        langEx = ".en"
    elif preferredLanguage == "en":
        langEx = ".en"
    elif preferredLanguage == "fr":
        langEx = ".fr"
    elif preferredLanguage == "de":
        langEx = ".de"
    elif preferredLanguage == "es":
        langEx = ".es"
    elif preferredLanguage == "fa":
        langEx = ".fa"
    else :
        langEx = ""
    filename = filename + langEx
    return filename



def readHeaders(tcpSocket):
    message = tcpSocket.recv(4096).decode('utf-8')
    print ("Client request: ", message)
    pData = message.split('\r\n')[0]
    dict = header2dict(message)
    dict.update({"STATUS-LINE":pData})
    return [dict, pData]
    #fullRequest = message.split('\r\n')

    #queryData = fullRequest[0]
    #checkPostData = True

    # dict = {
    #     "STATUS-LINE" : ""
    # }
    # dict = dict.update({"STATUS-LINE": queryData})
    # print dict

    # for header in fullRequest:
    #     if checkPostData :
    #         queryData = header
    #         checkPostData = False
    #     else :
    #         headerLine = header.split(":")
    #         if len(headerLine) > 1:
    #
    #
    # print queryData
def sendFile(tcpSocket, fileLang, type, seconds):
    # tcpSocket.send('HTTP/1.0 200 OK\n')
    # tcpSocket.send('Content-Type: %s\n' % type)
    # tcpSocket.send('Accept-Language: %s\n' % lang)
    # file = open(lang,'rb') # open file , r => read , b => byte format
    # response = file.read()
    # file.close()
    # tcpSocket.send(response.encode('utf-8'))
    if (fileLang == ''):
        fileLang = 'index.html'

    file = open(fileLang,'r') # open file , r => read
    response = file.read()
    file.close()
    header = 'HTTP/1.1 200 OK\n'
    header += 'Content-Type: '+type+'\n\n'
    final_response = header.encode('utf-8')
    final_response += response
    tcpSocket.send(final_response)



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
            filename = headers["STATUS-LINE"].split()[1].lstrip('/')
            print "Status Line: " , headers["STATUS-LINE"]
            filenameLanguage = acceptLanguageModifyFile(filename, headers)
            seconds = None
            # if filenameLanguage == filename:
            #    seconds = ifModifiedSinceSeconds(headers)
            sendFile(connectionSocket, filenameLanguage, "text/html", seconds)
            # connectionSocket.shutdown(SHUT_WR)
            connectionSocket.close()
        except IOError:
            print "Not found %s" % filename
            print IOError
            sendError(connectionSocket, '404','Not Found')
            connectionSocket.shutdown(SHUT_WR)
            connectionSocket.close()
        except KeyboardInterrupt:
            print "\n Interrupted by CTRL-C"
            break
    serverSocket.close()

main()

