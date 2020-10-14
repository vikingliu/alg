from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import Proxy, ProxyType

import time
import json

user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
# options = webdriver.ChromeOptions()
# 设置无头模式
# options.add_argument("--headless")
# options.add_argument('user-agent="%s"' % user_agent)
# options.add_argument('accept-encoding="gzip, deflate, br"')
# options.add_argument('accept-language="zh-CN, zh;"')
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option('useAutomationExtension', False)


# def custom_response(req, req_body, res, res_body):
#     import gzip
#
#     if req.path.find('7cLOtPi5wrHA') > 0:
#         res_body = gzip.decompress(res_body)
#         if res_body.find(b'selenium') > 0:
#             # res_body = res_body.replace(b'selenium', b'x')
#             res_body = gzip.compress(res_body)
#             print('modify 7cLOtPi5wrHA.js')
#             return res_body

# if req.path.find('.js') > 0:
#     res_body = gzip.decompress(res_body)
#     if res_body.find(b'debugger') > 0:
#         res_body = res_body.replace(b'debugger;', b'')
#         res_body = gzip.compress(res_body)
#         print('modify ' + req.path)
#         return res_body
#
# seleniumwire_options = {
#     'custom_response_handler': custom_response,
# }

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


# driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
#     "source": """
#     Object.defineProperty(navigator, 'webdriver', {
#       get: () => undefined
#     })
#   """
# })


def ali_trademark(keyword):
    q = {"classification": "", "product": "", "keyword": keyword, "searchType": "1", "status": "10", "pageNum": 1,
         "pageSize": 20}
    q = json.dumps(q)

    url = 'https://tm.aliyun.com/channel/search#/search?q=' + q
    driver.get(url)

    # WebDriverWait(driver, 60).until(EC.visibility_of_element_located(
    #     (By.XPATH, './/span[@class="next-input next-input-single next-input-large clear"]/input')))
    # input = driver.find_element_by_xpath('.//span[@class="next-input next-input-single next-input-large clear"]/input')
    # input.send_keys('nike')
    # input.send_keys(Keys.ENTER)
    res = []
    for i in range(3):
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable(
            (By.CLASS_NAME, "next-btn.next-btn-normal.next-btn-medium.next-pagination-item.next")))
        trademarks = driver.find_elements_by_xpath('.//div[@class="next-row trademark-row"]')
        for item in trademarks:
            title = item.find_element_by_class_name('info-title')
            additional = item.find_element_by_class_name('info-additional')
            img = item.find_element_by_xpath('.//div[@class="trademark-img"]//img')
            a = item.find_element_by_xpath('.//div[@class="trademark-img"]/a')
            people = item.find_element_by_xpath(
                './/div[@class="next-col next-col-fixed-11 trademark-label"]/div[1]/a[2]')
            date = item.find_element_by_xpath('.//div[@class="next-col next-col-fixed-11 trademark-label"]/div[2]/a[2]')
            status = item.find_element_by_xpath('.//span[@class="status-valid"]')
            product = item.find_element_by_xpath('.//div[@class="trademark-product"]/div[2]/a')
            trademark = [title.text, status.text, additional.text, people.text, date.text, product.text,
                         img.get_attribute('src'), a.get_attribute('href')]
            res.append(trademark)
            print(trademark)
        next_page = driver.find_element_by_xpath(
            './/button[@class="next-btn next-btn-normal next-btn-medium next-pagination-item next"]')
        next_page.click()

    driver.close()
    return res


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
            time.sleep(3)
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


if __name__ == '__main__':
    # ali_trademark('nike')
    official_trademark('阿里')
    # wipo('nike')
