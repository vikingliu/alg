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
    # 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    # 'accept-encoding': 'gzip, deflate, br',
    # 'accept-language': 'en-US, en;',
    'cookie': '_uab_collina=159973882043370406229731; _bl_uid=eIkLbeg9w10rjL6OOxwjy3zumjzs; XSRF-TOKEN=e20f6ef6-8535-4d94-b827-5f2602b6046c; x5sec=7b2261652d676c6f7365617263682d7765623b32223a223065613732373037313333646632313138623931346237666334316133643335434b76737a2f7346454e612f72662b346b4b615058513d3d227d; JSESSIONID=AA1BF4C45A87978E493956BC66E4034F; JSESSIONID=CEABBDC6467CAE2E7E08AFF033AD1A69'
}

# headers['cookie'] += '; aep_usuc_f=site=glo&c_tp=GBP&region=UK&b_locale=en_US; '

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
    else:
        with open('ali_translate.csv', 'w') as w:
            w = csv.writer(w)
            w.writerow(['id', 'language', 'url', 'title', 'desc'])
    n = 2000 - len(ids)
    while len(urls) < n:
        link = random.choice(links)
        urls.add(link)
    with open('ali_translate.csv', 'w') as w:
        w = csv.writer(w)
        for i, url in enumerate(urls):
            print(i + 1, url)
            rst = crawl_infos(url)
            w.writerows(rst)


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

        for lang, url in lang_urls.items():
            line = [id, lang, url]
            line += crawl_info(url)
            rst.append(line)
            print(url)
            print(line)
    return rst


def crawl_info(url):
    page = crawl_util.crawl(url)
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
    return ['', '']


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
