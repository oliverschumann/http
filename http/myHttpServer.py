'''
Created on 26.05.2013

@author: admin
'''
import string,cgi,time
from os import curdir,sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer


class BaseRequestHandler(BaseHTTPRequestHandler):
    pass

def main():
    print("starting http-server on port 80...")
    try:
        server = HTTPServer(('', 80), BaseRequestHandler)
    except KeyboardInterrupt:
        print("^C shutting down server...")
        server.socket.close()

if __name__ == '__main__':
    main()