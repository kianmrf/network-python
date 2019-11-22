import base64
import copy
import thread
import socket
import sys
import os
import datetime
import time
import json
import threading
import email.utils as eut

# global variables
max_connections = 10
BUFFER_SIZE = 4096
CACHE_DIR = "./cache"
BLACKLIST_FILE = ""
MAX_CACHE_BUFFER = 3
NO_OF_OCC_FOR_CACHE = 2
blocked = []
logs = {}
locks = {}

def main():
    if not os.path.isdir(CACHE_DIR):
    os.makedirs(CACHE_DIR)

    f = open(BLACKLIST_FILE, "rb")
    data = ""
    while True:
        chunk = f.read()
        if not len(chunk):
            break
        data += chunk
    f.close()
    blocked = data.splitlines()
    for file in os.listdir(CACHE_DIR):
        os.remove(CACHE_DIR + "/" + file)



def is_blocked(client_socket, client_addr, details):
    if not (details["server_url"] + ":" + str(details["server_port"])) in blocked:
        return False
    return True


# A thread function to handle one request
def handle_one_request_(client_socket, client_addr, client_data):

    details = parse_details(client_addr, client_data)

    if not details:
        print "no any details"
        client_socket.close()
        return

    isb = is_blocked(client_socket, client_addr, details)

    """
        Here we can check whether request is from outside the campus area or not.
        We have IP and port to which the request is being made.
        We can send error message if required.
    """

    if isb:
        print "Block status : ", isb

    if isb:
        client_socket.send("HTTP/1.0 200 OK\r\n")
        client_socket.send("Content-Length: 11\r\n")
        client_socket.send("\r\n")
        client_socket.send("Error\r\n")
        client_socket.send("\r\n\r\n")

    elif details["method"] == "GET":
        details = get_cache_details(client_addr, details)
        if details["last_mtime"]:
            details = insert_if_modified(details)
        serve_get(client_socket, client_addr, details)

    client_socket.close()
    print client_addr, "closed"
    print

def start_proxy_server():

    # Initialize socket
    try:
        proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        proxy_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        proxy_socket.bind(('', proxy_port))
        proxy_socket.listen(max_connections)

        print "Serving proxy on %s port %s ..." % (
            str(proxy_socket.getsockname()[0]),
            str(proxy_socket.getsockname()[1])
            )

    except Exception as e:
        print "Error in starting proxy server ..."
        print e
        proxy_socket.close()
        raise SystemExit


    # Main server loop
    while True:
        try:
            client_socket, client_addr = proxy_socket.accept()
            client_data = client_socket.recv(BUFFER_SIZE)

            print
            print "%s - - [%s] \"%s\"" % (
                str(client_addr),
                str(datetime.datetime.now()),
                client_data.splitlines()[0]
                )

            thread.start_new_thread(
                handle_one_request_,
                (
                    client_socket,
                    client_addr,
                    client_data
                )
            )

        except KeyboardInterrupt:
            client_socket.close()
            proxy_socket.close()
            print "\nProxy server shutting down ..."
            break
