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


def taobao_shop():
    url = 'https://tmai.tmall.com/'
    cookie = 'cq=ccp%3D1; pnm_cku822=; t=b74955130ba2d54d99232e11d583c69f; _tb_token_=fea3e571b0de; cookie2=104655d521241bf6cf4f61d9e89f697d; cna=EF7KF1epo1gCAX0jZcrb8N/W; _m_h5_tk=b63634893534b0d805cbda69f3306c8f_1606983469408; _m_h5_tk_enc=e955176e1d973c697d8a76734b657ad5; uc1=cookie14=Uoe0az9p9Npo7g%3D%3D&cookie21=V32FPkk%2Fhw%3D%3D; csg=5b16ba1f; unb=2393890925; sn=%E5%B0%8F%E5%86%9B%E4%BA%8C%3Azhe; xlly_s=1; x5sec=7b2273686f7073797374656d3b32223a223632383336346135323266306265643036633438646633643034373330653338434d6a4d742f3446454953317037797a732f3374745145614444497a4f544d344f5441354d6a55374f413d3d227d; l=eBEdn81lORhkWZwFBOfZlurza779cIRfguPzaNbMiOCPOp1Mq3GVWZRIjpTHCnGVnsj9R38TDWZ7BlLLAy49hmuefEpEhYLg0dTh.; tfstk=cPzGB0s9Zv95ohi3VNg_ZXu1-ICRZ4vxEor38yMudKZjaAUFiCKe4YYCKAwgkn1..; isg=BHp6llPx8ThGT33UVXdQ4QBOy6acK_4F9TdY-4RzRY3AdxuxbLvZFEuFxwOrZ3ad'

    f = 'taobao_shop_urls.csv'
    find_cats = set()
    if os.path.exists(f):
        with open(f, 'r') as r:
            r = csv.reader(r)
            next(r)
            for row in r:
                find_cats.add(row[0])
    else:
        with open(f, 'w') as w:
            w = csv.writer(w)
            w.writerow(['cat', 'sale', 'rate', 'url'])
    try:
        driver.get(url)
        driver.delete_all_cookies()
        for item in cookie.split(';'):
            k, v = item.split('=', 1)
            driver.add_cookie({'name': k.strip(), 'value': v})
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, '//ul[@class="menu-list"]')))
        lis = driver.find_elements_by_xpath('//li[@class="menu popup-container"]')
        x = random.randint(0, len(lis)-1)
        lis[x].click()
        time.sleep(2)

        with open(f, 'a') as w:
            w = csv.writer(w)
            for xpath in ['//div[@class="skin-box-bd"]/ul/li[@class="cat fst-cat "]//li[@class="cat snd-cat  "]//a',
                          '//div[@class="skin-box-bd"]/ul/li[@class="cat fst-cat no-sub-cat "]//a']:
                get_cats_detail(w, xpath, find_cats)

    finally:
        driver.close()


def get_cats_detail(w, xpath, find_cats):
    cats = driver.find_elements_by_xpath(xpath)
    for i, cat in enumerate(cats):
        WebDriverWait(driver, 30).until(EC.visibility_of_element_located(
            (By.XPATH, '//div[@class="J_TItems"]')))
        cats = driver.find_elements_by_xpath(xpath)
        cat = cats[i]
        cat_name = cat.text
        if cat_name == '' or cat_name in find_cats:
            continue
        cat.click()
        details = get_details(cat_name)
        for detial in details:
            w.writerow([cat_name] + detial)
        print('%s/%s  cat:%s cnt:%s' % (i, len(cats), cat_name, len(details)))
        time.sleep(2)


def get_details(cat):
    details = []
    page = 1
    while True:
        WebDriverWait(driver, 30).until(EC.visibility_of_element_located(
            (By.XPATH, '//div[@class="J_TItems"]')))
        print(driver.current_url)
        # driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        items = driver.find_elements_by_xpath('//div[@class="J_TItems"]/div[@class="item4line1"]/dl')
        cnt = 0
        for item in items:
            a = item.find_element_by_xpath('.//dt[@class="photo"]/a[@class="J_TGoldData"]')
            sale = item.find_element_by_xpath('.//dd[@class="detail"]//div[@class="sale-area"]/span')
            rate = item.find_elements_by_xpath('.//dd[@class="rates"]/div[@class="title"]//span')
            if len(rate) == 0:
                continue
            detail = [sale.text, rate[0].text, a.get_attribute('href')]
            details.append(detail)
            cnt += 1
        print('cat: %s page:%s cnt:%s' % (cat, page, cnt))
        nexts = driver.find_elements_by_class_name('J_SearchAsync.next')
        if len(nexts) > 0:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                (By.CLASS_NAME, 'J_SearchAsync.next')))
            page += 1
            nexts[0].click()
            time.sleep(2)
        else:
            break
    return details


if __name__ == '__main__':
    get_chrome()
    taobao_shop()
