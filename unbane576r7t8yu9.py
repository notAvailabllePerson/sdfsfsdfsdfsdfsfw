import requests
import time
import sys
import os
import threading
import random
import autopy


class Work():

    def __init__(self):
        self.BLACK = '\033[30m'
        self.RED = '\033[31m'
        self.GREEN = '\033[32m'
        self.YELLOW = '\033[33m'
        self.BLUE = '\033[34m'
        self.MAGENTA = '\033[35m'
        self.CYAN = '\033[36m'
        self.WHITE = '\033[37m'
        self.UNDERLINE = '\033[4m'
        self.RESET = '\033[0m'

        self.done = 0
        self.error = 0

        self.startit()

    def startit(self):
        mainLogo = '''
███████╗██╗  ██╗ ██████╗  ██████╗██╗  ██╗██╗    ██╗ █████╗ ██╗   ██╗███████╗
██╔════╝██║  ██║██╔═══██╗██╔════╝██║ ██╔╝██║    ██║██╔══██╗██║   ██║██╔════╝
███████╗███████║██║   ██║██║     █████╔╝ ██║ █╗ ██║███████║██║   ██║█████╗  
╚════██║██╔══██║██║   ██║██║     ██╔═██╗ ██║███╗██║██╔══██║╚██╗ ██╔╝██╔══╝  
███████║██║  ██║╚██████╔╝╚██████╗██║  ██╗╚███╔███╔╝██║  ██║ ╚████╔╝ ███████╗
╚══════╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝  ╚═══╝  ╚══════╝
                            - dev by @9hea                                                       
        '''

        os.system('cls' if os.name == 'nt' else 'clear')

        print(self.BLUE+mainLogo)

        time.sleep(1)

        asklogo = '''
[1]. commercial band 

[2]. spam / violence
        '''
        print(self.RED+asklogo)

        asktype = int(input(self.GREEN+'[+]Chose 1/2 : '))

        if asktype == 1:
            self.askCrem()
        else:
            self.askspam()

    def askCrem(self):
        self.name = input(self.YELLOW+"[+] Full Name : ")
        self.username = str(input(self.YELLOW+"[+] Username : "))
        self.email = input(self.YELLOW+"[+] Email : ")
        self.reason = open("message.txt", 'r').read()
        self.country = str(input(self.YELLOW+"[+] country : "))
        self.sleep = int(input(self.YELLOW+"[+] sleep : "))

        self.useprx = str(input(self.BLUE+'[?] use proxies y/n : '))

        if self.useprx == 'y' or self.useprx == 'Y':
            self.prxfile = open('proxies.txt', 'r').read().splitlines()
            self.startcrem('yes')
        else:
            self.startcrem('no')

    def get_prx(self):

        prox = str(random.choice(self.prxfile))

        proxies = {
            'http': f'http://{prox}',
            'https': f'http://{prox}'
        }

        return proxies

    def printall(self):

        os.system('cls' if os.name == 'nt' else 'clear')

        cs = f'{self.GREEN} [+] Sent requests : {self.done} - {self.RED} [-] Bad requests : {self.error}'

        print(cs)

    def startcrem(self, prx):
        while True:

            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
                'sec-ch-ua': '^\\^',
                'content-type': 'application/x-www-form-urlencoded',
                'accept': '*/*',
                'origin': 'https://help.instagram.com',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'referer': 'https://help.instagram.com/contact/1652567838289083',
                'accept-language': 'en-US,en;q=0.9,ar;q=0.8',
                'cookie': 'ig_did=2A2C2E5B-8950-4B27-BE83-3D34C4938FFD; mid=YEXbdAALAAEa4jSWz7F2peh-rOfc; ig_nrcb=1; datr=LFhHYM4Y4-Jo3_b1jN0KbxDi; csrftoken=5Yx3tETHRtMvTz74Yzt0ukwtYDW1Sgub; ds_user_id=46053659368; sessionid=46053659368^%^3Am0A3TweSMQU1TX^%^3A13; shbid=10949; shbts=1624035414.9856033; dpr=1.25',
            }

            data = {
                'jazoest': '2973',
                'lsd': 'AVo43knbfnQ',
                'AccountType': 'Personal',
                'name': self.name,
                'Field1489970557888767': self.username,
                'email': self.email,
                'Field236858559849125_iso2_country_code': '',
                'Field236858559849125': self.country,
                'support_form_id': '1652567838289083',
                'support_form_hidden_fields': '{"904224879693114":false,"495070633933955":false,"1489970557888767":false,"488955464552044":false,"236858559849125":false,"1638971086372158":true,"1615324488732156":true,"236548136468765":true}',
                'support_form_fact_false_fields': '^[^]',
                '__user': '0',
                '__a': '1',
                '__dyn': '7xe6Fo4OQ1PyUbFuC1swgE98nwgU6C7UW8xi642-7E2vwXx60kO4o3Bw5VCwjE3awbG782Cwooa81Vrzo5-0jx0Fwww6DwtU6e0D83mwaS0zE0I6aw',
                '__csr': '',
                '__req': '4',
                '__hs': '18801.PHASED:DEFAULT.2.0.0.0',
                'dpr': '1.5',
                '__ccg': 'GOOD',
                '__rev': '1004020875',
                '__s': '14x4s7:xt7qvn:rovru8',
                '__hsi': '6977014919209280450-0',
                '__comet_req': '0',
                '__spin_r': '1004020875',
                '__spin_b': 'trunk',
                '__spin_t': '1624462874'
            }

            if prx == 'yes':

                try:
                    response = requests.post(
                        'https://help.instagram.com/ajax/help/contact/submit/page', headers=headers, data=data, proxies=self.get_prx())
                    if "__rc" in response.text:
                        print(self.GREEN+f'Unbanned : @{self.username} !')
                        autopy.alert.alert(f'Unbanned : @{self.username} !')
                        input(self.RESET+"Enter to exit ... ")
                        exit()
                    else:
                        self.done += 1

                except:
                    self.error += 1
            else:
                response = requests.post(
                    'https://help.instagram.com/ajax/help/contact/submit/page', headers=headers, data=data)
                if "__rc" in response.text:
                    print(self.GREEN+f'Unbanned : @{self.username} !')
                    autopy.alert.alert(
                        f'Unbanned : @{self.username} !', "Hi Sir!")
                    input(self.RESET+"Enter to exit ... ")
                    exit()
                else:
                    self.done += 1
            self.printall()
            time.sleep(self.sleep)

    def askspam(self):
        self.name = input(self.YELLOW+"[+] Full Name : ")
        self.username = str(input(self.YELLOW+"[+] Username : "))
        self.email = input(self.YELLOW+"[+] Email : ")
        self.reason = open("message.txt", 'r').read()
        self.phone = input(self.YELLOW+"[+] PhoneNumber : ")

        self.sleep = int(input(self.YELLOW+"[+] sleep : "))

        self.useprx = str(input(self.BLUE+'[?] use proxies y/n : '))

        if self.useprx == 'y' or self.useprx == 'Y':
            self.prxfile = open('proxies.txt', 'r').read().splitlines()
            self.startspam('yes')
        else:
            self.startspam('no')

    def startspam(self, prx):

        while True:

            try:

                headers = {
                    'x-fb-lsd': 'AVo43knbsW8',
                    'sec-ch-ua-mobile': '?0',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
                    'sec-ch-ua': '^\\^',
                    'content-type': 'application/x-www-form-urlencoded',
                    'accept': '*/*',
                    'origin': 'https://help.instagram.com',
                    'sec-fetch-site': 'same-origin',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-dest': 'empty',
                    'referer': 'https://help.instagram.com/contact/606967319425038?helpref=page_content',
                    'accept-language': 'en-US,en;q=0.9,ar;q=0.8',
                    'cookie': 'ig_did=2A2C2E5B-8950-4B27-BE83-3D34C4938FFD; mid=YEXbdAALAAEa4jSWz7F2peh-rOfc; ig_nrcb=1; datr=LFhHYM4Y4-Jo3_b1jN0KbxDi; csrftoken=5Yx3tETHRtMvTz74Yzt0ukwtYDW1Sgub; ds_user_id=46053659368; sessionid=46053659368^%^3Am0A3TweSMQU1TX^%^3A13; shbid=10949; shbts=1624035414.9856033; dpr=1.25',
                }

                data = {
                    'jazoest': '2938',
                    'lsd': 'AVo43knbsW8',
                    'name': self.name,
                    'email': self.email,
                    'instagram_username': self.username,
                    'mobile_number': self.phone,
                    'appeal_reason': self.reason,
                    'support_form_id': '606967319425038',
                    'support_form_hidden_fields': '{}',
                    'support_form_fact_false_fields': '[]',
                    '__user': '0',
                    '__a': '1',
                    '__dyn': '7xe6Fo4OQ1PyUbFuC1swgE98nwgU6C7UW8xi642-7E2vwXx60kO4o3Bw5VCwjE3awbG782Cwooa81Vrzo5-0jx0Fwww6DwtU6e0D83mwaS0zE0I6aw',
                    '__csr': '',
                    '__req': 'j',
                    '__hs': '18801.PHASED:3ADEFAULT.2.0.0.0',
                    'dpr': '1.5',
                    '__ccg': 'GOOD',
                    '__rev': '1004020875',
                    '__s': 'adbzwr:3Axt7qvn:As7w1yn',
                    '__hsi': '6977023934631943752-0',
                    '__comet_req': '0',
                    '__spin_r': '1004020875',
                    '__spin_b': 'trunk',
                    '__spin_t': '1624464973'
                }

                if prx == 'yes':

                    response = requests.post(
                        'https://help.instagram.com/ajax/help/contact/submit/page', headers=headers, data=data)
                else:
                    response = requests.post(
                        'https://help.instagram.com/ajax/help/contact/submit/page', headers=headers, data=data, proxies=get_prx())
                if "layerCancel" in response.text:
                    print(self.GREEN+f'Unbanned : @{self.username} !')
                    autopy.alert.alert(
                        f'Unbanned : @{self.username} !', "Hi Sir!")
                    input(self.RESET+"Enter to exit ... ")
                    exit()
                else:
                    self.done += 1
                self.printall()
                time.sleep(self.sleep)

            except:
                self.error += 1
                self.printall()


if __name__ == '__main__':
    Work()
