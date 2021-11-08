# coding=utf-8
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
import urllib

driver = None


def get_chrome():
    global driver
    # user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15"
    options = webdriver.ChromeOptions()
    # 设置无头模式
    # options.add_argument("--headless")
    # options.add_argument('user-agent="%s"' % user_agent)
    # options.add_argument('cookie="%s"' % cookie)
    # options.add_argument("proxy-server=socks5://127.0.0.1:1080")
    # options.add_argument('accept-encoding="gzip, deflate, br"')
    # options.add_argument('accept-language="zh-CN, zh;"')
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options)
    js = open('stealth.min.js').read()
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": js
    })


def pdd():
    url = 'https://mobile.yangkeduo.com/'
    driver.get(url)
    cookie = " pdd_vds=gaZLvIfNcoBNuLBndGxbvbemxblNeidICQltBbcydiZQBOxQuLYLdadETmfE; rec_list_personal=rec_list_personal_zjbz6p; PDDAccessToken=U2DOZVMSNBGF4GGMXZ7OKD2DJV5ALP4OZTOOSFSLRPPZH4THN2PA113b87e; pdd_user_id=6694759959480; pdd_user_uin=S4LSJW4IXJY7Z3ZR7HCMC624MI_GEXDA; JSESSIONID=DFF2E231671BE8814252E4760A57D782; ua=Mozilla%2F5.0%20(Macintosh%3B%20Intel%20Mac%20OS%20X%2010_15_7)%20AppleWebKit%2F605.1.15%20(KHTML%2C%20like%20Gecko)%20Version%2F14.0%20Safari%2F605.1.15; webp=0; _nano_fp=XpEanqg8X5EJn0Tql9_jsTJBmozCOoAt0FNUcHJE; api_uid=Cktlvl+3vPx3vwBNcpgVAg=="
    # ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
    # ua = urllib.parse.quote(ua)
    ua = None
    driver.delete_all_cookies()
    for item in cookie.split(';'):
        k, v = item.split('=', 1)
        if k.strip() == 'ua' and ua:
            v = ua
        # driver.add_cookie({'name': k.strip(), 'value': v})
    urls = get_urls()
    cnt = 0
    for url in urls:
        driver.get(url)
        cnt += 1
        print(cnt, url)
        r = random.randint(10, 30)
        time.sleep(r)
        # time.sleep(1000)


def taobao_search():
    cookie = open('tb.cookie', 'r').read()
    # cookie = '_samesite_flag_=true; cookie2=18a9df5ea3074414f54ef074ebaea70c; t=eca561ef3fa5cf3aa1372f0a69a3d105; _tb_token_=5eeb9b13637bf; cna=2IAFGVUYmz0CAXs6delvfZ1t; xlly_s=1; hng=CN%7Czh-CN%7CCNY%7C156; thw=cn; unb=35333237; lgc=liuhuang007; cookie17=UNX4F9dVlcc%3D; dnk=liuhuang007; tracknick=liuhuang007; _l_g_=Ug%3D%3D; sg=77a; _nk_=liuhuang007; cookie1=V32VxQ7i5H%2FoVBEON4pYoHvW4P3tegYtj096Lb0Pb1c%3D; sgcookie=E100dFFfGZlMEsL25mPqq3syIKYtdG55oQCVneX0cF0XycU6oA26lA9pSgSyTFxfIPlWKlLSdz5Nq9x2BcJZ7F0gKQ%3D%3D; uc3=nk2=D8rzHFeu5uRjtfI%3D&vt3=F8dCuwpjuyPhywF0Cbc%3D&lg2=V32FPkk%2Fw0dUvg%3D%3D&id2=UNX4F9dVlcc%3D; csg=e59a4036; skt=729600c9eed55ed2; existShop=MTYxODk4NTc4OQ%3D%3D; uc4=id4=0%40UgJ99TgYSpzI1Jc57q3naBuw4A%3D%3D&nk4=0%40DenJvgGMV7R6fAirAyXmjvw7juLzkw%3D%3D; _cc_=WqG3DMC9EA%3D%3D; mt=ci=2_1; uc1=pas=0&existShop=false&cookie21=U%2BGCWk%2F7p4mBoUyS4plD&cookie15=UIHiLt3xD8xYTw%3D%3D&cookie14=Uoe1iunaXt%2B8xA%3D%3D&cookie16=U%2BGCWk%2F74Mx5tgzv3dWpnhjPaQ%3D%3D; enc=VvxjmfXaW1z48BOwmnDrxzq9F1pzpaKjkJVxcZHlGGwW3zx7Nlg4hyfsZ3X6YWkjtQW3F3gbz9GYiwbYoJmybg%3D%3D; JSESSIONID=2BDA2FF0FF427C15CE4F49D7CAD0E6C7; l=eBTr9hy4OdRyhMkEBOfZnurza77OSIRxmuPzaNbMiOCPOK1p5FoOW6ahJCT9C3hVh6oBR3lcJ54LBeYBcIv4n5U62j-la_kmn; tfstk=c5ahBQspiA9fQKigcwgQOQGlg9SOZhp-nurg7zvKM6eTgS4NiaKw0xY1Ivw3y31..; isg=BFVVgYbCmeuA8oIdPw_IYbwnZFcPUglkrbnF49f6EEwbLnUgn6BoNQPs-TKYEiEc'
    driver.get('https://s.taobao.com/')
    driver.delete_all_cookies()
    for item in cookie.split(';'):
        k, v = item.split('=', 1)
        driver.add_cookie({'name': k.strip(), 'value': v})

    cnt = 0
    while True:
        cnt += 1
        url = 'https://s.taobao.com/search?initiative_id=staobaoz_20210421&q=only%E5%AE%98%E6%96%B9%E6%97%97%E8%88%B0%E5%BA%97&suggest=0_2&_input_charset=utf-8&wq=onl&suggest_query=onl&source=suggest'
        print(cnt, url)
        driver.get(url)
        r = random.randint(5, 15)
        time.sleep(r)
        new_cookie = [c.get("name", '')+'='+c.get('value', '') for c in driver.get_cookies()]
        new_cookie = ';'.join(new_cookie)
        print(new_cookie)
        f = open('tb.cookie', 'w')
        f.write(new_cookie)


def get_urls():
    f = open('pdd_url.csv')
    urls = [url.strip() for url in f.readlines()]
    return urls


if __name__ == '__main__':
    get_chrome()
    # pdd()
    taobao_search()
