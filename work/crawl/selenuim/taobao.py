# from selenium import webdriver
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import time
import logging
user_agent = "User-Agent=Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
options = webdriver.ChromeOptions()

# options.add_argument('ignore-certificate-errors')
# options.add_argument('disable-infobars')
# options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-running-insecure-content')
options.add_argument("--disable-web-security")
# options.add_experimental_option('excludeSwitches', ['ignore-certificate-errors'])
# options.add_argument('allow-running-insecure-content')
# 设置无头模式
# options.add_argument("--headless")
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)
# options.add_argument(user_agent)
driver = webdriver.Chrome(options=options)


# safari
# driver = webdriver.Safari(seleniumwire_options={'port': 12345})



#firefox
# options = webdriver.FirefoxOptions()
# # profile = webdriver.FirefoxProfile()
# # profile.accept_untrusted_certs = True
# cap = DesiredCapabilities.FIREFOX
# # cap["marionette"] = False
# cap['acceptSslCerts'] = False
# # options.headless = True
# driver = webdriver.Firefox(capabilities=cap, options=options)

# #
# dcap = dict(DesiredCapabilities.PHANTOMJS)
# dcap["phantomjs.page.settings.userAgent"] = user_agent
# driver = webdriver.PhantomJS(desired_capabilities=dcap) #无界面浏览器


def taobao():
    # driver.rewrite_rules =[
    #     # (r'http.*wake.js', 'file:///Users/liuhuang/learn/github/alg/work/crawl/selenuim/wake.js')
    # ]

    driver.get("https://market.m.taobao.com/app/tmall-def/jhsbybt/web/index.html")
    # driver.get("https://gw.alicdn.com/tfs/TB1zkbOd8FR4u4jSZFPXXanzFXa-180-176.png?getAvatar=avatar_110x10000.jpg")
    js = '''
      for(i in document.scripts){
            script = document.scripts[i];
            console.log(script.src);
            if(script.src == "https://g.alicdn.com/mtb/lib-smb-wake/0.0.90/wake.js"){
               script.src =  "";
            }
      }
    '''

    # js = 'clearTimeout()'
    # driver.execute_script(js)
    # input.send_keys("python")
    #
    # input.send_keys(Keys.ENTER)


    # wait.until(EC.presence_of_element_located((By.ID,'content_left')))
    # 输出响应信息

    print(driver.current_url)
    for request in driver.requests:
        if request.url.find('avatar_110x10000.jpg') > 0:
            print(request.response.body)
    # print(driver.get_cookies())
    # WebDriverWait(driver, 20).until(...)
    cnt = 0
    while True:
        time.sleep(10)
        #
        cnt += 1
        tab_click(driver)
        if cnt == 10:
            break

def tab_click(driver, timeout=2, texts=None, operation={}):
    """
    点击某个组件
    :param driver:
    :param timeout:
    :param operation:
    :return:
    """
    items_list = []
    # if operation and 'by' in operation:
    #     if operation['by'] == By.CLASS_NAME:
    #         ecs = driver.find_elements_by_class_name(operation['by_value'])
    #     elif operation['by'] == By.XPATH:
    #         ecs = driver.find_elements_by_xpath(operation['by_value'])

    ecs = driver.find_elements_by_class_name('tabItemFix__label_text')
    for ec in ecs:
        if ec.text and ec.text != '':
            tab = ec.text.encode('utf8', errors='ignore')
            if not texts or tab in texts:
                try:
                    logging.info("start click tab=%s", tab)
                    ec.click()
                    time.sleep(timeout)
                    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

                    # driver.page_source.encode('utf8', errors='ignore')
                except Exception as e:
                    print(e)
                    logging.exception("%s", e)
    return items_list

def baidu():
    driver.get("https://www.baidu.com")
    # 查找id值为kw的节点对象（搜索输入框）
    input = driver.find_element_by_id("kw")
    # 模拟键盘输入字串内容
    input.send_keys("python")
    # 模拟键盘点击回车键
    input.send_keys(Keys.ENTER)
    # 显式等待,最长10秒
    wait = WebDriverWait(driver, 10)
    # 等待条件：10秒内必须有个id属性值为content_left的节点加载出来，否则抛异常。
    wait.until(EC.presence_of_element_located((By.ID, 'content_left')))
    # 输出响应信息
    print(driver.current_url)
    # print(driver.get_cookies())
    # print(driver.page_source)

try:

    taobao()

finally:
    #关闭浏览器
    # driver.close()
    pass