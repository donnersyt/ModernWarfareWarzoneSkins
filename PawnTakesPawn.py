import requests
import string
import random
from faker import Faker
fake = Faker()
from mail import MailBox
import uuid
from bs4 import BeautifulSoup as bs
import threading

class PawnTakesPawn:
    def __init__(self, User, Email):
        self.s = requests.session()
        self.User = User
        self.Email = Email
        self.currentCSRF = ""

    def updateCSRF(self, pageResponse):
        try:
            self.currentCSRF = bs(pageResponse, "html.parser").find({"input":"_csrf_token"})["value"]
        except:
            self.currentCSRF = ""
            print("Failed to update CSRF!")

    def loadSignUpPage(self):
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'en-GB,en;q=0.9',
            'authority': 'pawntakespawn.com',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
        }
        response = self.s.get('https://pawntakespawn.com/registration/new', headers=headers)
        self.updateCSRF(response.content)
        #print(response.status_code)
        return response.content


    def createAccount(self):
        headers = {
            'authority': 'pawntakespawn.com',
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'origin': 'https://pawntakespawn.com',
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'referer': 'https://pawntakespawn.com/registration/new',
            'accept-language': 'en-GB,en;q=0.9',
    }

        data = {
            "_csrf_token": self.currentCSRF,
            "user[first_name]": self.User.name.split(" ")[0],
            "user[last_name]": self.User.name.split(" ")[-1],
            "user[username]": self.Email.prefix,
            "user[email]": self.Email.email,
            "user[email_confirmation]": self.Email.email,
            "user[password]": "password",
            "user[password_confirmation]": "password",
            "user[country]": "GB",
            "user[birthday][month]": self.User.month,
            "user[birthday][day]": self.User.day,
            "user[birthday][year]": self.User.year,
            "user[accept_terms]": "true"
        }

        response = self.s.post('https://pawntakespawn.com/registration', headers=headers, data=data)

        # print(response.text)
        # print(response.status_code)
        if (response.url != "https://pawntakespawn.com/registration"): # if it redirects, account was made
            return True
        else: # if not, was an error. email used? username used?
            return False

    def confirmEmail(self, url):
        headers = {
            'authority': 'pawntakespawn.com',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-dest': 'document',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'
        }
        response = self.s.get(url, headers=headers)
        self.updateCSRF(response.content)
        if (response.url == "https://pawntakespawn.com/session/new"):
            return True
        else:
            return False

    def login(self):
        headers = {
            'authority': 'pawntakespawn.com',
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'origin': 'https://pawntakespawn.com',
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'referer': 'https://pawntakespawn.com/session/new',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'
        }
        data = {
            '_csrf_token': self.currentCSRF,
            'user[email]': self.Email.email,
            'user[password]': "password"
        }
        response = self.s.post('https://pawntakespawn.com/session', headers=headers, data=data)
        # print(response.status_code)
        # print(response.url)
        if (response.url == "https://pawntakespawn.com/achievements"):
            return True
        else:
            return False

    def loadTheTruths(self):
        headers = {
            'authority': 'pawntakespawn.com',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'
        }
        response = self.s.get('https://pawntakespawn.com/invisibletruths', headers=headers)
        self.updateCSRF(response.content)

    def sendTheTruths(self):
        headers = {
            'authority': 'pawntakespawn.com',
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'origin': 'https://pawntakespawn.com',
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'referer': 'https://pawntakespawn.com/invisibletruths',
            'accept-language': 'en-GB,en;q=0.9'
        }
        data = {
            '_csrf_token': self.currentCSRF,
            'code1': 'FUGAZIFILE',
            'code2': 'INFOHAX',
            'code3': 'BURNBAG',
            'code4': 'SHREDITALL',
            'code5': 'INTELFIRE',
            'code6': 'GRIDSQUARE'
        }
        response = self.s.post('https://pawntakespawn.com/invisibletruths', headers=headers, data=data)
        # print(response.status_code)
        # print(response.url)

    def fetchCodeToRedeem(self):
        headers = {
            'authority': 'pawntakespawn.com',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'referer': 'https://pawntakespawn.com/achievements',
            'accept-language': 'en-GB,en;q=0.9'
        }

        response = self.s.get('https://pawntakespawn.com/advancedpawn', headers=headers)
        code = bs(response.content, "html.parser").find_all("h1")[-1].string
        return code


class randomUser:
    def __init__(self):
        self.name = fake.name()
        self.month = str(random.randint(1,12))
        self.day = str(random.randint(1,28))
        self.year = str(random.randint(1960, 2000))


def saveCode(code):
    if code is not None:
        with open("codes.txt", "a+") as f:
            f.write("%s\n" % (code))

def getCode():
    while True:
        user = randomUser()
        email = MailBox()

        instance = PawnTakesPawn(user, email)
        signupPage = instance.loadSignUpPage()
        res = instance.createAccount()
        k = 0
        while email.checkMessagePawnTakesPawn() == False:
            print("Waiting for email...")
            time.sleep(2)
            if k == 10:
                print("Restarting Task")
                getCode()
        confirmUrl = email.getConfirmUrl()
        instance.confirmEmail(confirmUrl)
        instance.login()
        instance.loadTheTruths()
        instance.sendTheTruths()
        codeToRedeem = instance.fetchCodeToRedeem()
        codes.append(codeToRedeem)
        saveCode(codeToRedeem)
    #return codeToRedeem



codes = []
for i in range(1):
    t = threading.Thread(target=getCode,).start()

import time

while True:
    print(codes)
    time.sleep(3)