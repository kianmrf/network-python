import copy
import thread
import sys
import os
import datetime
import time
import json
import threading
from socket import socket, SOCK_STREAM, AF_INET
import webbrowser
import urllib2

# global variables
max_connections = 10
BUFFER_SIZE = 4096
# local directory to keep the cached data
CACHE_DIR = "./cache"
# note that blocked urls are included in the following txt file
BLACKLIST_FILE = "blacklist.txt"
MAX_CACHE_BUFFER = 3
NO_OF_OCC_FOR_CACHE = 2
blocked = []
logs = {}
locks = {}



def prepare():
    if not os.path.isdir(CACHE_DIR):
        os.makedirs(CACHE_DIR)

    # f = open(BLACKLIST_FILE, "rb")
    # data = ""
    # while True:
    #     chunk = f.read()
    #     if not len(chunk):
    #         break
    #     data += chunk
    # f.close()
    # blocked = data.splitlines()
    for file in os.listdir(CACHE_DIR):
        os.remove(CACHE_DIR + "/" + file)

# insert the header
def insert_if_modified(details):

    lines = details["client_data"].splitlines()
    while lines[len(lines)-1] == '':
        lines.remove('')

    #header = "If-Modified-Since: " + time.strptime("%a %b %d %H:%M:%S %Y", details["last_mtime"])
    header = time.strftime("%a %b %d %H:%M:%S %Y", details["last_mtime"])
    header = "If-Modified-Since: " + header
    lines.append(header)

    details["client_data"] = "\r\n".join(lines) + "\r\n\r\n"
    return details

# determine if a certain URL is blocked by Admin
def is_blocked(client_socket, client_addr, details):
    if not (details["server_url"] + ":" + str(details["server_port"])) in blocked:
        return False
    return True


# returns a dictionary of details in a request
def parse_details(client_addr, client_data):
    try:
        # parse first line like below
        # http:://127.0.0.1:20020/1.data

        lines = client_data.splitlines()
        while lines[len(lines)-1] == '':
            lines.remove('')
        first_line_tokens = lines[0].split()
        url = first_line_tokens[1]

        # get starting index of IP
        url_pos = url.find("://")
        if url_pos != -1:
            protocol = url[:url_pos]
            url = url[(url_pos+3):]
        else:
            protocol = "http"

        # get port if any
        # get url path
        port_pos = url.find(":")
        path_pos = url.find("/")
        if path_pos == -1:
            path_pos = len(url)


        # change request path accordingly
        if port_pos==-1 or path_pos < port_pos:
            server_port = 80
            server_url = url[:path_pos]
        else:
            server_port = int(url[(port_pos+1):path_pos])
            server_url = url[:port_pos]

        # build up request for server
        first_line_tokens[1] = url[path_pos:]
        lines[0] = ' '.join(first_line_tokens)
        client_data = "\r\n".join(lines) + '\r\n\r\n'

        return {
            "server_port" : server_port,
            "server_url" : server_url,
            "total_url" : url,
            "client_data" : client_data,
            "protocol" : protocol,
            "method" : first_line_tokens[0],
        }

    except Exception as e:
        print e
        return None


def get_requests(details):
    client_data = details["client_data"]
    #do_cache = details["do_cache"]
    #cache_path = details["cache_path"]
    #last_mtime = details["last_mtime"]

    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.connect((details["server_url"], details["server_port"]))
    server_socket.send(details["client_data"])

    reply = server_socket.recv(BUFFER_SIZE)

    print (reply)



#Create a TCP socket
#Notice the use of SOCK_STREAM for TCP packets
def main():
    prepare()
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
            message = connectionSocket.recv(4096).decode('utf-8')
            print ("Client request: ", message)
            string_list = message.split(' ')
            method = string_list[0]
            requesting_url = string_list[1]

            print('Client request ',requesting_url.split("://")[1].split("/")[0])
            details = parse_details(addr, message)
            get_requests(details)



            #connectionSocket.close()
        except IOError:
            header = 'HTTP/1.1 404 Not Found\n\n'
            response = '<html><body><center><h3>Error 404: File not found</h3></center></body></html>'.encode('utf-8')
            final_response = header.encode('utf-8')
            final_response += response
            connectionSocket.send(final_response)
            connectionSocket.close()

        except KeyboardInterrupt:
            print ("\nInterrupted by CTRL-C")
            break
    serverSocket.close()


main()
