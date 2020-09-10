# from selenium import webdriver
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import time
import logging

# user_agent = "User-Agent=Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
options = webdriver.ChromeOptions()
# 设置无头模式
# options.add_argument("--headless")
options.add_argument('user-agent="%s"' % user_agent)
options.add_argument('accept-encoding="gzip, deflate, br"')
options.add_argument('accept-language="zh-CN, zh;"')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=options)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined
    })
  """
})
driver.delete_all_cookies()

# safari
# driver = webdriver.Safari(seleniumwire_options={'port': 12345})


# firefox
# options = webdriver.FirefoxOptions()
# profile = webdriver.FirefoxProfile()
# profile.accept_untrusted_certs = True
# cap = DesiredCapabilities.FIREFOX
# cap["marionette"] = False
# cap['acceptSslCerts'] = False
# options.headless = True
# driver = webdriver.Firefox(capabilities=cap, options=options)


def taobao():
    driver.get("https://market.m.taobao.com/app/tmall-def/jhsbybt/web/index.html")
    print('wait the page')
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CLASS_NAME, "rax-view.tabItemFix__label")))
    print('I am ok')
    ecs = driver.find_elements_by_class_name('rax-view.tabItemFix__label')
    for idx in range(len(ecs)):
        ecs = driver.find_elements_by_class_name('rax-view.tabItemFix__label')
        ecs[idx].click()
        time.sleep(3)
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(3)
    driver


def pdd():
    driver.get('https://yangkeduo.com/')
    WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CLASS_NAME, "X51cAr_2")))
    print('I am ok')
    ec = driver.find_element_by_class_name('X51cAr_2')
    ec.click()
    WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CLASS_NAME, "wE02A8Ay")))
    print('I am ok')
    time.sleep(3)
    ecs = driver.find_elements_by_class_name('wE02A8Ay')
    for i in range(len(ecs)):
        ecs = driver.find_elements_by_class_name('wE02A8Ay')
        ecs[i].click()
        time.sleep(3)
        tabs = driver.find_elements_by_class_name('_35U5JtfD')
        sub_tabs = tabs[i].find_elements_by_class_name('_3JH3uODQ')

        if sub_tabs:

            for j in range(len(sub_tabs)):
                sub_tabs = tabs[i].find_elements_by_class_name('_3JH3uODQ')
                sub_tabs[j].click()
                time.sleep(3)
        # driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(3)


def ali():
    driver.get('https://www.aliexpress.com/')
    time.sleep(100)


def amazon():
    driver.get('https://www.amazon.com/')
    WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.ID, "nav-hamburger-menu")))
    nav = driver.find_element_by_ID('nav-hamburger-menu')
    nav.click()
    time.sleep(100)


if __name__ == '__main__':
    taobao()
    # pdd()
    # ali()
    # amazon()
