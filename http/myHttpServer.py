'''
Created on 26.05.2013

@author: admin
'''
import string,cgi,time,Cookie,csv
import hashlib

from os import curdir,sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer


class BaseRequestHandler(BaseHTTPRequestHandler):
    secureToken = []
    
    def sendFileToBrowser(self, fileName, statusCode=200, contentType="text/html"):
        f = open(fileName)
        self.send_response(statusCode)
        self.send_header("Content-Type", contentType)
        self.end_headers()
        self.wfile.write(f.read())
        f.close
        
    
    def do_showSignIn(self):
        fileName = curdir + sep + "files" + sep + "html" + sep + "loginform.html"
        self.sendFileToBrowser(fileName, statusCode=401)
    
    
    def checkUserNamePassport(self, userName, password):
        valid = False
        if userName != "":
            if password != "":
                reader = csv.reader(open(curdir + sep + "files" + sep + "user.csv", "rb"))
                for row in reader:
                    if row[0] == userName:
                        if row[1] == hashlib.sha512(password).hexdigest():
                            valid = True
                            break
        return valid
    
    
    def do_GET(self):
        try:
            sToken = ""
            if self.headers.has_key('cookie'):
                self.cookie = Cookie.SimpleCookie(self.headers.getheader("cookie"))
                try:
                    sToken = self.cookie['sToken'].value
                    if len(sToken) > 0:
                        if sToken in self.secureToken:
                            pass
                        else:
                            sToken = ""
                        
                except:
                    sToken = ""
                
                
            if sToken == "":
                self.do_showSignIn()
                
            else:
                fileName = "index.html"
                if len(self.path) > 1:
                    position = self.path.rfind("/")
                    if position != -1:
                        position = position + 1
                        fileName = self.path[position:]
                    
                filePathName = curdir + sep + "files" + sep + "html" + sep + fileName
                self.sendFileToBrowser(filePathName)

        except IOError:
            pass
            
    def do_POST(self):
        """
        Erlaubte POST-Ziele:
            /login.php
        """
        try:
            """
            Daten anhand des Content-Type ermitteln und zur Verfuegung stellen
            """
            postvars = {}
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                postvars = cgi.parse_multipart(self.rfile, pdict)
            elif ctype == 'application/x-www-form-urlencoded':
                length = int(self.headers.getheader('content-length'))
                postvars = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
            else:
                postvars = {}
            
            """
            Ziele 
            """
            if self.path.endswith("/login.php"):
                userName = str(postvars['user'][0]).lower()
                password = str(postvars['password'][0])
                
                self.send_response(301)
                redirectTo = "/loginform.html"
                if self.checkUserNamePassport(userName, password) == True:
                    secureTokenValue = hashlib.sha512(hashlib.md5(password).hexdigest() + userName).hexdigest()
                    self.secureToken.append(secureTokenValue)
                    c = Cookie.SimpleCookie()
                    c['sToken'] = secureTokenValue
                    self.send_header('Set-Cookie', c.output(header=''))
                    redirectTo = "/index.html"
                    
                self.send_header("Location", redirectTo)
                self.end_headers()
            
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
