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
BLACKLIST_FILE = "blacklist.txt"
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
    start_proxy_server()

# lock fileurl
def get_access(fileurl):
    if fileurl in locks:
        lock = locks[fileurl]
    else:
        lock = threading.Lock()
        locks[fileurl] = lock
    lock.acquire()

# unlock fileurl
def leave_access(fileurl):
    if fileurl in locks:
        lock = locks[fileurl]
        lock.release()
    else:
        print "Lock problem"
        sys.exit()

def is_blocked(client_socket, client_addr, details):
    if not (details["server_url"] + ":" + str(details["server_port"])) in blocked:
        return False
    return True


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


# if cache is full then delete the least recently used cache item
def get_space_for_cache(fileurl):
    cache_files = os.listdir(CACHE_DIR)
    if len(cache_files) < MAX_CACHE_BUFFER:
        return
    # """"
    # last_mtime = min(os.path.getmtime(CACHE_DIR + "/" + file) for file in cache_files)
    # print last_mtime
    # file = [file for file in cache_files if os.path.getmtime(CACHE_DIR + "/" + file) == last_mtime][0]
    # print file
    # os.remove(CACHE_DIR + "/" + file)
    # print file, "removed"
    # """
    last_mtime = min(logs[file][-1]["datetime"] for file in cache_files)
    file_to_del = [file for file in cache_files if logs[file][-1]["datetime"] == last_mtime][0]

    os.remove(CACHE_DIR + "/" + file_to_del)


# check whether file is already cached or not
def get_current_cache_info(fileurl):
    cache_path = CACHE_DIR
    if fileurl.startswith("/"):
        fileurl = fileurl.replace("/", "", 1)

    for dir in fileurl.split(":"):
        if not os.path.isdir(dir):
            os.makedirs(dir)
            cache_path = cache_path +"/" +dir
        else:
            continue
    #cache_path = CACHE_DIR + "/" + fileurl.replace("/", "__")

    if os.path.isfile(cache_path):
        last_mtime = time.strptime(time.ctime(os.path.getmtime(cache_path)), "%a %b %d %H:%M:%S %Y")
        return cache_path, last_mtime
    else:
        return cache_path, None

# collect all cache info
def get_cache_details(client_addr, details):
    get_access(details["total_url"])
    #add_log(details["total_url"], client_addr)
    do_cache = True
    cache_path, last_mtime = get_current_cache_info(details["total_url"])
    leave_access(details["total_url"])
    details["do_cache"] = do_cache
    details["cache_path"] = cache_path
    details["last_mtime"] = last_mtime
    return details

# serve get request
def serve_get(client_socket, client_addr, details):
    try:
        #print details["client_data"], details["do_cache"], details["cache_path"], details["last_mtime"]
        client_data = details["client_data"]
        do_cache = details["do_cache"]
        cache_path = details["cache_path"]
        last_mtime = details["last_mtime"]

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((details["server_url"], details["server_port"]))
        server_socket.send(details["client_data"])

        reply = server_socket.recv(BUFFER_SIZE)
        if last_mtime and "304 Not Modified" in reply:
            print "returning cached file %s to %s" % (cache_path, str(client_addr))
            get_access(details["total_url"])
            f = open(cache_path, 'rb')
            chunk = f.read(BUFFER_SIZE)
            while chunk:
                client_socket.send(chunk)
                chunk = f.read(BUFFER_SIZE)
            f.close()
            leave_access(details["total_url"])

        else:
            if do_cache:
                print "caching file while serving %s to %s" % (cache_path, str(client_addr))
                get_space_for_cache(details["total_url"])
                get_access(details["total_url"])
                f = open(cache_path, "w+")
                # print len(reply), reply
                while len(reply):
                    client_socket.send(reply)
                    f.write(reply)
                    reply = server_socket.recv(BUFFER_SIZE)
                    #print len(reply), reply
                f.close()
                leave_access(details["total_url"])
                client_socket.send("\r\n\r\n")

        server_socket.close()
        client_socket.close()
        return

    except Exception as e:
        server_socket.close()
        client_socket.close()
        print e
        return


# returns a dictionary of details
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



# A thread function to handle one request
def handle_one_request_(client_socket, client_addr, client_data):

    details = parse_details(client_addr, client_data)

    if not details:
        print "no any details"
        client_socket.close()
        return

    isb = is_blocked(client_socket, client_addr, details)

    # check if requested URL is blocked

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
    proxy_port = 2525

    try:
        proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        proxy_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        proxy_socket.bind(('', proxy_port))
        proxy_socket.listen(max_connections)

        print "Serving proxy on localhost port %s ..." % (
            str(proxy_socket.getsockname()[0])
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

main()
