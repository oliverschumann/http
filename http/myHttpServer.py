'''
Created on 26.05.2013

@author: admin
'''
import string,cgi,time,Cookie,csv
from os import curdir,sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer


class BaseRequestHandler(BaseHTTPRequestHandler):
    
    def sendFileToBrowser(self, fileName, statusCode=200, contentType="text/html"):
        f = open(fileName)
        self.send_response(statusCode)
        self.send_header("Content-Type", contentType)
        
        c = Cookie.SimpleCookie()
        c['value'] = "1234"
        self.send_header('Set-Cookie', c.output(header=''))

        self.end_headers()
        self.wfile.write(f.read())
        f.close
        
    
    def do_showSignIn(self):
        fileName = curdir + sep + "files" + sep + "html" + sep + "loginform.html"
        self.sendFileToBrowser(fileName)
    
    def checkUserNamePassport(self, userName, password):
        valid = False
        if username != "":
            if password != "":
                reader = csv.reader(open(curdir + sep + "files" + sep + "user.csv", "rb"))
                for row in reader:
                    pass
                valid = True
        return valid
    
    def do_GET(self):
        try:
            #ctype, pdict = cgi.parse_header(self.headers.getheader('cookie',""))
            ctype = ""
            if self.headers.has_key('cookie'):
                self.cookie = Cookie.SimpleCookie(self.headers.getheader("cookie"))
                ctype = self.cookie.values()
            if ctype == "":
                self.do_showSignIn()
            else:
                fileName = curdir + sep + "files" + sep + "html" + sep + "index.html"
                self.sendFileToBrowser(fileName)

        except IOError:
            self.send_error(404, "not found!")
            
    def do_POST(self):
        try:
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                postvars = cgi.parse_multipart(self.rfile, pdict)
            elif ctype == 'application/x-www-form-urlencoded':
                length = int(self.headers.getheader('content-length'))
                postvars = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
            else:
                postvars = {}
        except IOError:
            self.send_error(404, "not found!")
            
        self.send_response(301)
        self.send_header("Location", "/index.html")
        self.end_headers()
        

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