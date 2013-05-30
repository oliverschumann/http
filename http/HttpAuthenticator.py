'''
Created on 30.05.2013

@author: user
'''
import csv, hashlib, time

class HttpAuthenticator(object):
    '''
    classdocs
    '''
    passwordFilePath = ""
    secureTokenStore = []

    def __init__(self, passwordFilePath):
        self.passwordFilePath = passwordFilePath
    
    def isValidUserNamePassport(self, userName, password):
        valid = False
        loUsername = userName.lower()
        if userName != "":
            if password != "":
                reader = csv.reader(open(self.passwordFilePath, "rb"))
                for row in reader:
                    if row[0].lower() == loUsername:
                        if row[1] == hashlib.sha512(password).hexdigest():
                            valid = True
                            break
        return valid
    
    
    def generateSecureToken(self, userName, password):
        secureToken = hashlib.sha512(hashlib.md5(password + str(time.time())).hexdigest() + userName).hexdigest()
        self.secureTokenStore.append(secureToken)
        return secureToken
    
    
    def isValidToken(self, secureToken):
        valid = False
        if len(secureToken) > 0:
            valid = secureToken in self.secureTokenStore
        
        return valid