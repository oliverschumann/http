'''
Created on 26.05.2013

@author: admin
'''
import string,cgi,time
from os import curdir,sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer


class BaseRequestHandler(BaseHTTPRequestHandler):
    
    def sendFileToBrowser(self, fileName, statusCode=200, contentType="text/html"):
        f = open(fileName)
        self.send_response(statusCode)
        self.send_header("Content-Type", contentType)
        self.end_headers()
        self.wfile.write(f.read())
        f.close
        
    
    def do_signIn(self):
        fileName = curdir + sep + "files" + sep + "html" + sep + "loginform.html"
        self.sendFileToBrowser(fileName)
    
    def do_GET(self):
        try:
            ctype, pdict = cgi.parse_header(self.headers.getheader('cookie',""))
            if ctype == "":
                self.do_signIn()

        except IOError:
            self.send_error(404, "not found!")

def main():
    print("starting http-server on port 80...")
    try:
        server = HTTPServer(('', 80), BaseRequestHandler)
        print("started server!")
        server.serve_forever()
        
    except KeyboardInterrupt:
        print("^C shutting down server...")
        server.socket.close()

if __name__ == '__main__':
    main()