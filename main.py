from threading import Thread
import multiprocessing
from gmail import *
import configparser
from loguru import logger
import time
from filesystem import *


def run(thread_name):
    logger.info(f"[{thread_name}] started.")
    while True:
        if cookies_queue.empty() is True:
            logger.warning("Cookies queue is empty. Thread complete.")
            return
        Gmail(cookies_queue.get(), proxies_queue.get(), thread_name)


if __name__ == "__main__":
    multiprocessing.freeze_support()
    config = configparser.ConfigParser()
    config.read('config.ini')
    threads_count = int(config['SETTINGS']['Threads'])
    get_cookies()
    get_proxies()
    logger.info(f"Threads - {threads_count} pcs")
    logger.info(f"Cookies - {cookies_queue.qsize()} pcs")
    logger.info("Press Enter to start")
    input()
    run("THREAD-1")
    for i in range(threads_count):
        Thread(target=run, args=(f"THREAD-{i}",)).start()
    while True:
        time.sleep(1)

