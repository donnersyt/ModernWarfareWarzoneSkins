import requests
import random
import uuid
from bs4 import BeautifulSoup as bs

class MailBox:
    def __init__(self):
        self.baseUrl = "https://www.1secmail.com/api/v1/"
        self.prefix = uuid.uuid4().hex[0:12]
        #self.prefix = "hello"
        self.messageID = None
        self.email = self.prefix + "@1secmail.com"

        self.params = {
            "login": self.prefix,
            "domain": "1secmail.com"
        }

    def checkMessagePawnTakesPawn(self):
        params = self.params.copy()
        params["action"] = "getMessages"

        a = requests.get(self.baseUrl, params=params)
        res = a.json()
        for item in res:
            if "pawntakespawn" in item["from"]:
                self.messageID = item["id"]
                return item["id"]
            else:
                pass
        return False

    
    def getConfirmUrl(self):
        params = self.params.copy()
        params["action"] = "readMessage"
        params["id"] = self.messageID

        a = requests.get(self.baseUrl, params=params)
        res = a.json()["body"]
        url = bs(res, "html.parser").find("a")["href"]
        return url
        

# a = MailBox()
# ID = a.checkMessagePawnTakesPawn()