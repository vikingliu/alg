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
retry = 0
not_found_ids = {}


def ali_trademark():
    f = 'douyin_trademark.csv'
    find_keys = set()
    if os.path.exists(f):
        with open(f, 'r') as r:
            r = csv.reader(r)
            next(r)
            for row in r:
                find_keys.add(row[0])
    else:
        with open(f, 'w') as w:
            w = csv.writer(w)
            w.writerow(['id', 'brand', 'status', 'cate', 'people', 'date', 'product', 'logo', 'detail'])

    keys = load_ids()
    # 1 商标名，2 注册号，3 申请人
    search_type = "2"
    # 0 全部，10 已注册
    trademark_status = "0"

    not_found = 0
    max_page = 3
    with open(f, 'a') as w:
        w = csv.writer(w)
        for i, key in enumerate(keys):
            if key.startswith('#'):
                not_found = 0
                continue
            if key in find_keys:
                not_found = 0
                continue
            if not_found_ids.get(key, 0) > 1:
                print('real not found ' + key)
                continue

            url = get_url(key, trademark_status, search_type)
            driver.get(url)
            for page in range(max_page):
                if not is_aliyun_ready():
                    # w.writerow([key] + [''] * 8)
                    print('not found ' + key)
                    not_found += 1
                    if key not in not_found_ids:
                        not_found_ids[key] = 0
                    not_found_ids[key] += 1
                    if not_found == 3:
                        print('yes I am dead...')
                        driver.close()
                        return False
                    break
                not_found = 0
                trademarks = driver.find_elements_by_xpath('.//div[@class="next-row trademark-row"]')
                for item in trademarks:
                    title = item.find_element_by_class_name('info-title')
                    additional = item.find_element_by_class_name('info-additional')
                    cate_id = additional.text.split('注册号：')
                    img = item.find_element_by_xpath('.//div[@class="trademark-img"]//img')
                    a = item.find_element_by_xpath('.//div[@class="trademark-img"]/a')
                    people = item.find_element_by_xpath(
                        './/div[@class="next-col next-col-fixed-11 trademark-label"]/div[1]/a[2]')
                    date = item.find_element_by_xpath(
                        './/div[@class="next-col next-col-fixed-11 trademark-label"]/div[2]/a[2]')
                    status = item.find_element_by_xpath('.//span[@class="status-valid"]')
                    product = item.find_element_by_xpath('.//div[@class="trademark-product"]/div[2]/a')
                    trademark = [cate_id[1], title.text, status.text, cate_id[0], people.text, date.text, product.text,
                                 img.get_attribute('src'), a.get_attribute('href')]
                    print(i + 1, trademark)
                    w.writerow(trademark)

                if len(trademarks) == 20:
                    path = './/footer//div[@class="next-pagination-pages"]/button[@class="next-btn next-btn-normal next-btn-medium next-pagination-item next"]'
                    next_page = driver.find_elements_by_xpath(
                        path)
                    next_page[0].click()
                else:
                    break
            time.sleep(0.5)

    driver.close()
    return True


def get_url(key, status="10", search_type="1"):
    q = {"classification": "", "product": "", "keyword": key, "searchType": search_type, "status": status, "pageNum": 1,
         "pageSize": 20, "image": "", "fileName": ""}
    q = json.dumps(q)
    q = urllib.parse.quote(q, safe='/', encoding='utf-8', errors=None)
    url = 'https://tm.aliyun.com/channel/search#/search?q=' + q
    return url


def is_aliyun_ready():
    global retry
    while True:
        try:
            WebDriverWait(driver, 8).until(EC.visibility_of_element_located(
                (By.CLASS_NAME, "info-title")))
            return True
        except:
            frame = driver.find_elements_by_id('baxia-dialog-content')
            verfiy = False
            if len(frame) > 0:
                frame = frame[0]
                driver.switch_to.frame(frame)
                div = driver.find_elements_by_id("nc_1_n1z")
                verfiy = True
                if len(div) > 0:
                    div = div[0]
                    tracks = get_tracks(300)
                    ActionChains(driver).move_to_element(div)
                    for i in range(10, 400, 40):
                        x = i + random.randint(0, 40)
                        y = round(random.uniform(1.0, 5.0), 1)
                        ActionChains(driver).move_to_element_with_offset(to_element=div, xoffset=x, yoffset=y).perform()
                        t = random.uniform(0, 1.0)
                        time.sleep(t)

                    for i in range(400, 40, -40):
                        x = i + random.randint(-40, 0)
                        y = round(random.uniform(1.0, 5.0), 1)
                        ActionChains(driver).move_to_element_with_offset(to_element=div, xoffset=x, yoffset=y).perform()
                        t = random.uniform(0, 1.0)
                        time.sleep(t)

                    time.sleep(1)

                    print('unlock the verify bar')
                    ActionChains(driver).click_and_hold(on_element=div).perform()
                    tracks = get_tracks(258)
                    for i in tracks:
                        y = 0
                        ActionChains(driver).move_by_offset(xoffset=i, yoffset=y).perform()
                    time.sleep(2)

                    verfiy = True
                    ActionChains(driver).click_and_hold(on_element=div).release()
                    errors = driver.find_elements_by_class_name('nc-lang-cnt')
                    if len(errors) > 0 and errors[0].is_displayed():
                        retry += 1
                        print('unlock error ....')
                    if retry > 3:
                        return False
                    close = driver.find_elements_by_class_name('baxia-dialog-close')
                    if close:
                        close[0].click()
                else:
                    print('no verify bar')
                    center = driver.find_elements_by_xpath('.//center')
                    if len(center) > 0:
                        if '500 Internal Server Error' in center[0].text:
                            print('500 Internal Server Error')
                            return False
            else:
                print('no iframe')
            if verfiy:
                print('reload current page')
                driver.switch_to.parent_frame()
                driver.refresh()
            else:
                return False


def get_tracks(length):
    tracks = []
    start = 10
    while length > 0:
        track = random.randint(start, start + 40)
        if track > length:
            track = length
        tracks.append(track)
        length -= track
        start += 10
        # if random.random() > 0.8:
        #     back = random.randint(0, 2)
        #     if back > 0:
        #         length += back
        #         tracks.append(-back)
    print(tracks)
    return tracks


def official_trademark(keyword):
    url = 'http://sbj.cnipa.gov.cn/sbcx/'
    # url = 'http://wcjs.sbj.cnipa.gov.cn/txnS02.do?locale=zh_CN&kmcmNx0Q=qGq7cakdddddddddduBePRGY5x4FZKpvJAFzndMv.i0qqHZ'
    res = []
    driver.get(url)
    WebDriverWait(driver, 60).until(EC.element_to_be_clickable(
        (By.XPATH, './/img[@complete="complete"]')))

    print('index page load')
    btn = driver.find_element_by_xpath('.//img[@complete="complete"]')
    btn.click()
    WebDriverWait(driver, 60).until(EC.element_to_be_clickable(
        (By.XPATH, './/div[@class="icon_box"]/img')))
    print('search page load')
    btns = driver.find_elements_by_xpath('.//div[@class="icon_box"]/img')
    if len(btns) > 1:
        btns[1].click()
    time.sleep(1)
    driver.delete_all_cookies()
    inputs = driver.find_elements_by_xpath('.//div[@class="inputbox"]/input')
    if inputs:
        inputs[0].click()
        # for c in cate:
        #     inputs[0].send_keys(c)
        time.sleep(1)
        inputs[2].click()
        for c in keyword:
            inputs[2].send_keys(c)
            time.sleep(1)
        btn = driver.find_element_by_id('_searchButton')
        time.sleep(1)
        btn.click()
        time.sleep(3)
        tabs = driver.window_handles
        driver.switch_to.window(tabs[-1])
        WebDriverWait(driver, 60).until(EC.visibility_of_element_located(
            (By.XPATH, './/tr[@class="ng-scope"]')))
        print('search results page load')
        items = driver.find_elements_by_xpath('.//tr[@class="ng-scope"]')
        for i, item in enumerate(items):
            values = item.find_elements_by_class_name('lwtd%s' % (i % 2))
            for j, value in enumerate(values):
                # if j == 1:
                #     value.click()
                print(value.text, end=' ')
            # time.sleep(3)
            print('')
    time.sleep(100)
    driver.close()
    return res


def wipo(keyword):
    url = 'https://www3.wipo.int/branddb/en/'
    driver.get(url)
    WebDriverWait(driver, 60).until(EC.visibility_of_element_located(
        (By.ID, 'BRAND_input')))
    text = driver.find_element_by_id('BRAND_input')
    text.send_keys(keyword)
    btn = driver.find_element_by_xpath('.//div[@class="searchButtonContainer bottom right"]/a')

    btn.click()
    time.sleep(100)


def get_chrome():
    global driver
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36"
    options = webdriver.ChromeOptions()
    cookie = 'cna=EF7KF1epo1gCAX0jZcrb8N/W; xlly_s=1; __yunlog_session__=1605023156518; aliyun_choice=CN; _ga=GA1.2.291216055.1605023158; _gid=GA1.2.585379561.1605023158; _bl_uid=tkk4Lh0qcLs5pdc3LintlXO7F16L; _gat_gtag_UA_159056470_1=1; tfstk=cba5BdAQBJUq-ujez71qajIBuKoOZMKiOaM7NuFsm0KObjF5iATZCwFLKK8xXj1..; l=eBQNr3jIOFw-mh8kXOfZlurza77OSIRYHuPzaNbMiOCPOHBH5GV1WZSMPJKMC3hVh6oJR3J6Kkf8BeYBcIYmFjLnZWdg7Pkmn; isg=BISEZ2gSh9xEYDPSLtRR8d6PVQR2nagHzsdwOJ4lEM8SySSTxq14l7prCGERC-Bf'
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
    driver.delete_all_cookies()


def get_firefox():
    global driver
    # firefox
    options = webdriver.FirefoxOptions()
    profile = webdriver.FirefoxProfile()
    cap = DesiredCapabilities.FIREFOX
    # options.headless = True
    proxy = Proxy({
        'proxyType': ProxyType.MANUAL,
        'httpProxy': 'http://helo_crm_liuhongxia.mandy:zPtTv2LwbznHLcTc@10.124.155.190:8080',
        'httpsProxy': 'https://helo_crm_liuhongxia.mandy:zPtTv2LwbznHLcTc@10.124.155.190:8080',
        'no_proxy': ''
    })
    driver = webdriver.Firefox(capabilities=cap, options=options)
    # driver = webdriver.Firefox(options=options, seleniumwire_options=seleniumwire_options)
    driver.delete_all_cookies()


def get_safari():
    pass


def load_ids():
    ids = []
    for line in open('ids.txt').readlines():
        ids.append(line.strip())
    return ids


if __name__ == '__main__':
    while True:
        retry = 0
        try:
            get_chrome()
            # get_firefox()
            if ali_trademark():
                break
            # official_trademark('阿里')
            # wipo('nike')
        except Exception as e:
            driver.close()
            print(e)
