import os
from queue import Queue

cookies_queue = Queue()
proxies_queue = Queue()


def get_cookies():
    for folder in os.listdir("Cookies"):
        for sub_solder in os.listdir(f"Cookies\\{folder}"):
            with open(f"Cookies\\{folder}\\{sub_solder}\\Gmail_Good_Cookies.txt", "r") as f:
                cookies_queue.put(f.read())


def get_proxies():
    with open("proxies.txt") as f:
        proxies = f.read().split("\n")
    for i in range(10000):
        for proxy in proxies:
            proxies_queue.put({"https": f"http://{proxy}/", "http": f"http://{proxy}/"})