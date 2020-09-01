#coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

#初始化一个浏览器（如：谷歌，使用Chrome需安装chromedriver）
#下载 https://chromedriver.storage.googleapis.com/index.html
#chromedriver 放置到/usr/local/bin/目录下

options = webdriver.ChromeOptions()
# options.add_argument('--ignore-certificate-errors')

driver = webdriver.Chrome(options=options)
# 下载 https://phantomjs.org/download.html
# phantomjs 放到 /usr/local/bin/目录下
# driver = webdriver.PhantomJS() #无界面浏览器
try:
    #请求网页
    driver.get("https://market.m.taobao.com/app/tmall-def/jhsbybt/web/index.html")
    #查找id值为kw的节点对象（搜索输入框）
    # input = driver.find_element_by_id("kw")
    # #模拟键盘输入字串内容
    # input.send_keys("python")
    # #模拟键盘点击回车键
    # input.send_keys(Keys.ENTER)
    # #显式等待,最长10秒
    # wait = WebDriverWait(driver,10)
    # #等待条件：10秒内必须有个id属性值为content_left的节点加载出来，否则抛异常。
    # wait.until(EC.presence_of_element_located((By.ID,'content_left')))
    # # 输出响应信息
    # print(driver.current_url)
    # print(driver.get_cookies())
    # print(driver.page_source)
finally:
    #关闭浏览器
    #driver.close()
    pass
