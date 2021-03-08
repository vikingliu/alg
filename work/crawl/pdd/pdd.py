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
    cookie = 'api_uid=Ck2PmGARcz49mABfcZzIAg==; _nano_fp=XpEaXpmyn5XynqEbXC_gTuaMcQOzXIqdpyYolz9z; JSESSIONID=9CF233EBE564849F5E1099715D38E515; ua=Mozilla%2F5.0%20(Macintosh%3B%20Intel%20Mac%20OS%20X%2010_15_7)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F88.0.4324.96%20Safari%2F537.36; webp=1; PDDAccessToken=7HWU4CVSDYQWOJLY4SCQYFD5VBWAMGK4XXAUFF3P2K5XTP5SWFGQ113b87e; pdd_user_id=6694759959480; pdd_user_uin=S4LSJW4IXJY7Z3ZR7HCMC624MI_GEXDA; rec_list_personal=rec_list_personal_s6gm07; pdd_vds=gaLDNxGnGlbetntmiwIDPbtNQnONPLiGNunxownTnwPwosndbbbBoxNsaLLm'
    driver.get(url)
    driver.delete_all_cookies()
    for item in cookie.split(';'):
        k, v = item.split('=', 1)
        driver.add_cookie({'name': k.strip(), 'value': v})
    driver.get(url)
    time.sleep(100)
    driver.close()


if __name__ == '__main__':
    get_chrome()
    get_detail('https://yangkeduo.com')
