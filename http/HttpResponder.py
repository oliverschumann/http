'''
Created on 31.05.2013

@author: admin
'''
from os import curdir,sep

class HeatingHttpResponder(object):

    handler = None
    
    def __init__(self, httpRequestHandler):
        self.handler = httpRequestHandler
        
    def showInfo(self):
        print("Info...")
        self.handler.sendFileToBrowser(curdir + sep + "files" + sep + "html" + sep + "heatingstatus.html")
        