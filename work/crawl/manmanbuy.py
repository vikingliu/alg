# coding=utf-8

import crawl_util
import re
from lxml import html
import json


def crawl_cates():
    url = 'http://home.manmanbuy.com/bijia.aspx'
    page = crawl_util.crawl(url)
    content = page.text.encode('utf-8')
    sel = html.document_fromstring(content, parser=html.HTMLParser(encoding='utf-8'))
    lefts = sel.xpath('//div[@style="float:left;width:470px;"]')
    rights = sel.xpath('//div[@style="float:right;width:470px;"]')
    sku = {}
    for items in [lefts, rights]:
        if items:
            for ele in items[0].getchildren():
                if ele.tag == 'h2':
                    cat1 = ele.text
                    if cat1 not in sku:
                        sku[cat1] = {}
                elif ele.tag == 'div' and 'sclassBlock' == ele.attrib['class']:
                    divs = ele.getchildren()
                    cat2 = divs[0].text
                    if cat2 not in sku[cat1]:
                        sku[cat1][cat2] = {}
                    for cat3 in divs[1]:
                        if cat3.tag == 'a':
                            href = cat3.attrib['href']
                            name = cat3.text
                            if not name:
                                name = cat3.getchildren()[0].text
                            sku[cat1][cat2][name] = {'url': href}
    return sku


def crawl_list(url):
    page = crawl_util.crawl(url)
    content = page.text.encode('utf-8')
    cnt = re.findall(r'共有(\d+)条记录', content)
    return cnt[0] if cnt else 20


def crawl_all():
    sku = crawl_cates()
    i = 1
    for cat1, v1 in sku.items():
        for cat2, v2 in v1.items():
            for cat3, v3 in v2.items():
                url = v3['url']
                cnt = crawl_list(url)
                sku[cat1][cat2][cat3]['cnt'] = cnt
                print i, cnt, url
                i += 1

    sku = json.dumps(sku)
    with open('sku.txt', 'w') as w:
        w.write(sku)


def stats(sku=None):
    if not sku:
        with open('sku.txt', 'r') as r:
            txt = r.readline()
            sku = json.loads(txt)
    total = 0
    for cat1, v1 in sku.items():
        cnt = 0
        for cat2, v2 in v1.items():
            for cat3, v3 in v2.items():
                cnt += int(v3['cnt'])
        total += cnt
        print cat1, cnt
    print total


if __name__ == '__main__':
    stats()
    # crawl_all()
