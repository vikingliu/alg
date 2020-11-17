#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2020 Bytedance Inc. All Rights Reserved.
# Author:
'''
@File    :   browser_download_helper.py
@Author :
@Desciption :   None
@Modify Time :   2020-10-19 13:22
'''
import time
import os
import json
import logging
import bytedenv
import bytedmetrics
from seleniumwire import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from commodity_database_dig.dig.utils.util import retry
import re
from seleniumwire.proxy.handler import CaptureRequestHandler
from commodity_database_dig.dig.utils.tos_cache import TosCache
import commodity_database_dig.dig.utils.response_dict as response_dict
from urllib.parse import unquote
import numpy as np
import math
import random


try:
    from commodity_database_dig.dig.utils.util import get_settings
    spider_metrics = json.loads(get_settings('spider_metrics', 'temai.commodity_database.dig'))
    mtrics = bytedmetrics.Client(prefix=spider_metrics['browser_req'])
except Exception as e:
    logging.exception("%s", e)
    mtrics = bytedmetrics.Client()

response_dict._init()


class CacheCaptureRequestHandler(CaptureRequestHandler):

    static_pattern = re.compile(r'(.+)\.(css)(.*)')

    def check_need_cache(self, url):
        return self.static_pattern.match(url)

    def handle_request(self, req, req_body):
        # First make any modifications to the request
        req.body = req_body  # Temporarily attach the body to the request for modification
        self.modifier.modify_request(req, urlattr='path', methodattr='command')
        req_body = req.body
        need_cache = self.check_need_cache(req.path)
        hit_cache = False
        if need_cache:
            cache = TosCache(use_tos=True)
            content = cache.get(req.path)
            if content:
                req.need_cache = True
                req.cache_content = content
                req.path = 'http://127.0.0.1:4444'
                hit_cache = True
            else:
                logging.info('cache missed. url=%s', req.path)
        if not hit_cache:
            mtrics.emit_counter('throughput', 1, tags=dict(op="browser_req", ret="total"))
        else:
            mtrics.emit_counter('throughput', 1, tags=dict(op="browser_req", ret="cached"))
        return req_body

    def handle_response(self, req, req_body, res, res_body):
        # Make any modifications to the response
        self.modifier.modify_response(res, req, urlattr='path')
        if 'https://h5api.m.etao.com/h5/mtop.etao.fe.search/1.0/?' in req.path:
            path_dict = json.loads(unquote(req.path, 'utf-8').split('data=')[1])
            query = path_dict['q']
            response_dict.set_value('www.etao.com', query, res_body)
            logging.info("responsebody saved")
        if 'https://item-soa.jd.com/getWareBusiness?callback=jQuery' in req.path:
            source_item_id = unquote(req.path, 'utf-8').split('skuId=')[1].split("&")[0]
            response_dict.set_value('item.jd.com', source_item_id, res_body)
            logging.info("responsebody saved")
        if hasattr(req, 'cache_content'):
            return req.cache_content
        if hasattr(req, 'need_cache'):
            cache = TosCache(use_tos=True)
            cache.set(req.path, res_body)
            logging.info('save to cache, url=%s', req.path)
        if res and res.status == 200:
            mtrics.emit_counter('throughput', 1, tags=dict(op="browser_req", ret="success"))


class Response:
    content = None
    status_code = None


def init_chrome_driver(proxy, ua):
    """
    初始化浏览器
    :param proxies: list []
    :param h5:
    :return:
    """
    try:
        driver = None
        chrome_options = webdriver.ChromeOptions()
        # 以最高权限运行
        chrome_options.add_argument('--no-sandbox')
        # 不打开图形界面
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-dev-shm-usage')
        # 设置为开发者模式
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # 不加载图片，加快访问速度
        chrome_options.add_experimental_option('prefs', {"profile.managed_default_content_settings.images": 2})
        chrome_options.add_argument("blink-settings=imagesEnabled=false")
        chrome_options.add_experimental_option('useAutomationExtension', False)
        seleniumwire_options = {"proxy": {"no_proxy": "localhost,127.0.0.1"}}
        if proxy:
            proxy.update({"no_proxy": "localhost,127.0.0.1"})
            chrome_options.add_argument('--proxy-server={}'.format(proxy))
            seleniumwire_options = {"proxy": proxy}
        logging.info("seleniumwire_options ---> %s", seleniumwire_options)
        chrome_options.add_argument('user-agent={}'.format(ua))
        driver = webdriver.Chrome(
                seleniumwire_options=seleniumwire_options,
                # executable_path='chromedriver', chromedriver路径配置到PATH即可\
                options=chrome_options)
        driver._client._proxy.RequestHandlerClass = CacheCaptureRequestHandler
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                        Object.defineProperty(navigator, 'webdriver', {
                          get: () => undefined
                        })
                      """
        })
        driver.execute_cdp_cmd("Network.enable", {})
    except Exception as e:
        logging.exception("%s", e)
    return driver


@retry(0, 1)
def browser_crawl_detail(url, proxy, ua=None, browser='chrome', timeout=10, operation={}):
    """
    浏览器加载页面
    :param url:
    :param proxies: list []
    :param h5:
    :param browser:
    :return:
    """
    if not proxy:
        return None
    driver = None
    try:
        if browser == 'chrome':
            driver = init_chrome_driver(proxy, ua)
    except Exception as e:
        logging.exception("%s", e)
        raise e
    if driver:
        try:
            if url is not None:
                driver.get(url)
                time.sleep(timeout)
            if operation and 'by' in operation and operation['by'] and 'by_value' in operation and operation['by_value']:
                logging.info("operation=%s", operation)
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((operation['by'], operation['by_value'])))
        except Exception as e:
            logging.exception("download url by browser failed. except=%s url=%s", e, url)
    resp = Response()
    resp.content = driver.page_source
    resp.status_code = 200
    driver.quit()
    return resp


def ease_out_quad(x):
    return 1 - (1 - x) * (1 - x)


def ease_out_quart(x):
    return 1 - pow(1 - x, 4)


def ease_out_expo(x):
    if x == 1:
        return 1
    else:
        return 1 - pow(2, -10 * x)


def get_tracks(distance, seconds, ease_func):
    tracks = [0]
    offsets = [0]
    for t in np.arange(0.0, seconds, 0.1):
        ease = globals()[ease_func]
        offset = round(ease(t / seconds) * distance)
        tracks.append(offset - offsets[-1])
        offsets.append(offset)
    return offsets, tracks


# slider是要移动的滑块,tracks是要传入的移动轨迹
def move_to_gap(driver, slider, tracks):
    ActionChains(driver).click_and_hold(slider).perform()
    for x in tracks:
        ActionChains(driver).move_by_offset(xoffset=x,yoffset=0).perform()
    time.sleep(0.5)
    ActionChains(driver).release().perform()


@retry(0, 1)
def browser_crawl(url, trademark_id, proxy, ua=None, browser='chrome', timeout=10, operation={}):
    """
    浏览器加载页面
    :param url:
    :param proxies: list []
    :param h5:
    :param browser:
    :return:
    """
    if not proxy:
        return None
    driver = None
    try:
        if browser == 'chrome':
            driver = init_chrome_driver(proxy, ua)
    except Exception as e:
        logging.exception("%s", e)
        raise e
    if driver:
        duration = random.uniform(0.1, 0.4)
        get_tracks_ease = "ease_out_quart"
        try:
            aliyun_huakuai_verfiy = json.loads(get_settings("aliyun_huakuai_verfiy", "temai.commodity_database.dig"))
            duration = random.uniform(aliyun_huakuai_verfiy["duration"][0], aliyun_huakuai_verfiy["duration"][1])
            get_tracks_ease = aliyun_huakuai_verfiy["get_tracks_ease"]
        except Exception as e:
            logging.exception("%s", e)
        logging.info("trademark_id=%s duration=%s", trademark_id, duration)
        try:
            if trademark_id is not None:
                driver.get(url)
                time.sleep(3)
                input = driver.find_element_by_xpath('.//div[@class="next-select-inner"]/input')
                input.send_keys(trademark_id)
                input.send_keys(Keys.ENTER)
                time.sleep(3)
                current_pages = 1
                total_pages = 1
                while True:
                    retry = 5
                    while True:
                        if retry <= 0:
                            break
                        try:
                            iframe = driver.find_element_by_id("baxia-dialog-content")
                        except Exception as e:
                            break
                        # 滑动
                        try:
                            driver.switch_to.frame(iframe)
                            time.sleep(3)
                            huakuai = driver.find_element_by_xpath('//span[@id="nc_1_n1z"]')
                            if huakuai:
                                offsets, tracks = get_tracks(300, duration, 'ease_out_quart')
                                move_to_gap(driver, huakuai, tracks)
                        except Exception as e:
                            logging.exception("scroll failed. except=%s url=%s", e, url)
                        driver.switch_to.default_content()
                        try:
                            trademarks = driver.find_elements_by_xpath('.//div[@class="next-row trademark-row"]')
                            if trademarks:
                                break
                        except Exception as e:
                            logging.exception("click search failed. except=%s url=%s", e, url)
                        # 关闭对话框
                        try:
                            driver.find_element_by_xpath('//div[@class="baxia-dialog-close"]').click()
                            time.sleep(3)
                        except Exception as e:
                            logging.exception("click close failed. except=%s url=%s", e, url)
                        try:
                            trademarks = driver.find_elements_by_xpath('.//div[@class="next-row trademark-row"]')
                            if trademarks:
                                break
                        except Exception as e:
                            logging.exception("click search failed. except=%s url=%s", e, url)
                        # 搜索
                        try:
                            driver.find_element_by_xpath('//*[@class="next-btn next-btn-primary next-btn-large"]').click()
                            time.sleep(3)
                            trademarks = driver.find_elements_by_xpath('.//div[@class="next-row trademark-row"]')
                            if trademarks:
                                break
                        except Exception as e:
                            logging.exception("click search failed. except=%s url=%s", e, url)
                        retry -= 1

                    res = []
                    trademarks = driver.find_elements_by_xpath('.//div[@class="next-row trademark-row"]')
                    logging.info("search trademark_id={} ---> {}".format(trademark_id, trademarks))
                    for item in trademarks:
                        title = item.find_element_by_class_name('info-title')
                        additional = item.find_element_by_class_name('info-additional')
                        img = item.find_element_by_xpath('.//div[@class="trademark-img"]//img')
                        a = item.find_element_by_xpath('.//div[@class="trademark-img"]/a')
                        people = item.find_element_by_xpath(
                            './/div[@class="next-col next-col-fixed-11 trademark-label"]/div[1]/a[2]')
                        date = item.find_element_by_xpath(
                            './/div[@class="next-col next-col-fixed-11 trademark-label"]/div[2]/a[2]')
                        status = item.find_element_by_xpath('.//span[@class="status-valid"]')
                        product = item.find_element_by_xpath('.//div[@class="trademark-product"]/div[2]/a')
                        trademark = [title.text, status.text, additional.text, people.text, date.text, product.text,
                                     img.get_attribute('src'), a.get_attribute('href')]
                        res.append(trademark)
                        logging.info("trademark_id={} --> {}".format(trademark_id, trademark))
                    try:
                        total_pages = driver.find_element_by_xpath("//footer/div[@class='next-pagination next-pagination-normal next-pagination-arrow-only next-pagination-medium medium start inline-block']/div[@class='next-pagination-pages']/span[@class='next-pagination-display']")
                        current_pages = driver.find_element_by_xpath("//footer/div[@class='next-pagination next-pagination-normal next-pagination-arrow-only next-pagination-medium medium start inline-block']/div[@class='next-pagination-pages']/span[@class='next-pagination-display']/em")
                        logging.info("url=%s total_pages=%s current_pages=%s", url, total_pages.text, current_pages.text)
                        total_pages = int(total_pages.text.split("/")[-1])
                        current_pages = int(current_pages.text)
                        if total_pages > current_pages:
                            button = driver.find_element_by_xpath(
                                "//footer/div/div/button[@class='next-btn next-btn-normal next-btn-medium next-pagination-item next']")
                            button.click()
                        else:
                            break
                    except Exception as e:
                        logging.exception("%s", e)
                        break
                    time.sleep(3)
        except Exception as e:
            logging.exception("download url by browser failed. except=%s url=%s", e, url)
    resp = Response()
    resp.content = driver.page_source
    resp.status_code = 200
    resp.data = res
    driver.quit()
    return resp


if __name__ == '__main__':
    import time
    # from common_tools.common.util import init_logging_conf
    # init_logging_conf()
    #from commodity_database_dig.dig.const.proxy import choice_proxy
    #import random
    #pc_ua = json.loads(get_settings("pc_ua", "temai.commodity_database.dig"))
    #browser_crawl(trademark_id='49296006', ua=random.choice(pc_ua), proxy=random.choice(choice_proxy()))
    ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
    proxy = {'http': 'http://temai_tm_aliyun_dig:rWoR5CG7JZWlPw@10.120.4.41:8123', 'https': 'https://temai_tm_aliyun_dig:rWoR5CG7JZWlPw@10.120.4.41:8123'}
    url = '''https://tm.aliyun.com/channel/search#/search?q={"classification":"","product":"",
                    "keyword":"","searchType":"2","status":"0","pageNum":1,"pageSize":20,"image":"","fileName":""}'''
    #ret = browser_crawl(url=url, trademark_id='39507856', ua=ua, proxy=proxy)
    # url = """https://tm.aliyun.com/channel/search#/search?q={"classification":"","product":"",
    #                     "keyword":"","searchType":"1","status":"0","pageNum":1,"pageSize":20,"image":"","fileName":""}"""
    ret = browser_crawl(url=url, trademark_id="10442458", ua=ua, proxy=proxy)
    print(ret.data)
