# coding=utf-8
from lxml import html

import re
import time
import json
import csv
import os
import crawl_util
import random

headers = {
    # 'accept-encoding': 'gzip, deflate, br',
    # 'accept-language': 'en-US, en;',
    'cookie': '_uab_collina=160266968734004340056059; XSRF-TOKEN=4b92326e-5e92-420e-a7ca-fe2e8d3a1f46; _bl_uid=Fhkz4gq095L8my5OnjI5zCp92sh2; JSESSIONID=7272BA9A797C49E1FE53FF7E5973B3E3; JSESSIONID=97547A807D2DFCB920775463F4DF0EA4'
}

headers['cookie'] += '; aep_usuc_f=site=glo&c_tp=GBP&region=UK&b_locale=en_US; '

ali_catids = set()
links = []


def crawl_list(url, cate, page_key=0):
    page = crawl_util.crawl(url, headers=headers)
    content = page.content.decode('utf-8')
    infos = re.findall(r'window.runParams\s*=\s*(\{.*?\});', content)
    products = []
    dead = True
    total = 0
    if infos and len(infos) > 1:
        dead = False
        info = json.loads(infos[1])
        total = int(info.get('resultCount', '0'))
        for item in info.get('items', []):
            shop = item.get('store', {}).get('storeName', '')
            product = [cate, shop, item['title'], item.get('starRating', ''),
                       item.get('price', ''), item.get('tradeDesc', ''),
                       item.get('imageUrl', ''),
                       item.get('productDetailUrl', ''), info.get('resultCount', ''), page_key]
            products.append(product)
    print('products: %s' % len(products))
    return products, dead, total


def crawl_cates(url):
    page = crawl_util.crawl(url)
    content = page.content.decode('utf-8')
    sel = html.document_fromstring(content, parser=html.HTMLParser(encoding='utf-8'))
    links = sel.xpath('//div[@class="cg-main"]//li/a')
    cnt = len(links)
    with open('ali.csv', 'a') as w:
        w = csv.writer(w)
        for i, link in enumerate(links):
            url = 'https:' + link.attrib['href']
            items = url.split('/')
            name = items[-1].replace('.html', '')
            catid = items[-2]
            for page in range(1, 5):
                nextpage = url + '?trafficChannel=main&catName=%s&CatId=%s&ltype=wholesale&SortType=total_tranpro_desc&page=%s&isrefine=y' % (
                    name, catid, page)

                page_key = '%s-%s' % (catid, page)
                if page_key in ali_catids:
                    print('find ' + page_key)
                    continue
                print('%s/%s' % (i + 1, cnt), link.text, page, nextpage)
                products, dead, total = crawl_list(nextpage, name, page_key)
                if dead:
                    print('I am dead, reset cookie')
                    return
                if total < page * 60:
                    break
                w.writerows(products)
                time.sleep(2)
            # break


def crawl_translate_infos():
    urls = set()
    ids = set()
    if os.path.exists('ali_translate.csv'):
        with open('ali_translate.csv', 'r') as r:
            r = csv.reader(r)
            for product in r:
                ids.add(product[0])
                urls.add(product[2])
    else:
        with open('ali_translate.csv', 'w') as w:
            w = csv.writer(w)
            w.writerow(['id', 'language', 'url', 'title', 'desc'])
    n = 2000
    while len(urls) < n:
        link = random.choice(links)
        urls.add(link)
    with open('ali_translate.csv', 'a') as w:
        w = csv.writer(w)
        cnt = 0
        for i, url in enumerate(urls):
            print(i + 1, 'http:' +url)
            rst = crawl_infos(url)
            if rst:
                w.writerows(rst)
                cnt = 0
            else:
                cnt += 1
                if cnt > 3:
                    print('failed.... change cookie')
                    break


def crawl_infos(url):
    id = re.findall(r'(\d+).html', url)
    id = id[0] if id else 0
    rst = []
    if id != 0:
        lang_urls = {}
        ru = 'https://aliexpress.ru/item/%s.html' % (id)
        en = 'https://www.aliexpress.com/item/%s.html' % (id)
        lang_urls['en'] = en
        lang_urls['ru'] = ru
        for lang in ['id', 'ko', 'ar', 'de', 'es', 'fr', 'it', 'nl', 'pt', 'th', 'tr', 'vi', 'he', 'ja', 'pl']:
            lang_url = 'https://%s.aliexpress.com/item/%s.html' % (lang, id)
            lang_urls[lang] = lang_url
        tmp_headers = {'cookie': headers['cookie'] + '; aep_usuc_f=site=glo&c_tp=USD&region=US&b_locale=en_US;'}
        for lang, url in lang_urls.items():
            if lang not in ['en', 'id']:
                continue
            line = [id, lang, url]
            h = headers
            if lang == 'en':
                h = tmp_headers
            info = crawl_info(url, h)
            if info:
                line += info
            else:
                return None
            rst.append(line)
            print(url)
            print(line)
    return rst


def crawl_info(url, h=None):
    page = crawl_util.crawl(url, headers=h)
    content = page.content.decode('utf-8')
    infos = re.findall(r'window.runParams\s*=\s*(\{[\s\S]*?\});', content)
    info = infos[0] if infos else '{}'
    lines = info.split('\n')
    if len(lines) > 1:
        info = lines[1]
        info = info.replace('data:', '')
        info = info[:-1]
        info = json.loads(info)
        if 'pageModule' in info:
            title = info['pageModule']['title']
            desc = info['pageModule']['description']
            return [title, desc]
    with open('a.html', 'w') as w:
        w.write(content)
    return None


def read_csv():
    if os.path.exists('ali.csv'):
        with open('ali.csv', 'r') as r:
            r = csv.reader(r)
            for product in r:
                ali_catids.add(product[-1])
                links.append(product[-3])
    else:
        with open('ali.csv', 'w') as w:
            w = csv.writer(w)
            w.writerow(
                ['category', 'shop', 'title', 'starRating', 'price', 'trade', 'image', 'detail', 'sku', 'catid_page'])


if __name__ == '__main__':
    read_csv()
    # url = 'https://www.aliexpress.com/all-wholesale-products.html'
    # crawl_cates(url)
    crawl_translate_infos()
