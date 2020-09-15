# coding=utf-8
from lxml import html
import crawl_util
import re
import time
import json
import csv
import os

headers = {
    # 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    # 'accept-encoding': 'gzip, deflate, br',
    # 'accept-language': 'en-US, en;',
    'cookie': '_uab_collina=159973882043370406229731; _bl_uid=eIkLbeg9w10rjL6OOxwjy3zumjzs; XSRF-TOKEN=f88d5a11-8efa-43af-b7cc-c38e4426c3f1; x5sec=7b2261652d676c6f7365617263682d7765623b32223a223636636565386236383133663936626363323532366237306131393462353537434d57312f506f46454f333477623269743848373741453d227d; JSESSIONID=7EF117BAED5A3644CD838A493C8214CA; JSESSIONID=6312468F71DA54203BF2848448E79C5B'
}

headers['cookie'] += '; aep_usuc_f=site=glo&c_tp=GBP&region=UK&b_locale=en_US; '

ali_catids = set()


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


def read_csv():
    if os.path.exists('ali.csv'):
        with open('ali.csv', 'r') as r:
            r = csv.reader(r)
            for product in r:
                ali_catids.add(product[-1])
    else:
        with open('ali.csv', 'w') as w:
            w = csv.writer(w)
            w.writerow(
                ['category', 'shop', 'title', 'starRating', 'price', 'trade', 'image', 'detail', 'sku', 'catid_page'])


if __name__ == '__main__':
    read_csv()
    url = 'https://www.aliexpress.com/all-wholesale-products.html'
    crawl_cates(url)
    # url = 'https://www.aliexpress.com/category/200001648/blouses-shirts.html'
    # crawl_list(url)
