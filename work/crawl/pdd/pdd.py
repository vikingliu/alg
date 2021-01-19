from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.action_chains import ActionChains

import time
import json
import urllib
import os
import csv
import random
import traceback

driver = None


def get_chrome():
    global driver
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36"
    options = webdriver.ChromeOptions()
    # 设置无头模式
    # options.add_argument("--headless")
    # options.add_argument('user-agent="%s"' % user_agent)
    # options.add_argument('cookie="%s"' % cookie)

    # options.add_argument('accept-encoding="gzip, deflate, br"')
    # options.add_argument('accept-language="zh-CN, zh;"')
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options)

    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
          get: () => undefined
        })
      """
    })


def get_detail(url):
    driver.get(url)
    time.sleep(100)
    driver.close()


if __name__ == '__main__':
    get_chrome()
    get_detail('https://yangkeduo.com')
