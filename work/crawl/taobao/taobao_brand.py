# coding=utf-8

import urllib
import csv
import json
from lxml import html
import os
import sys

sys.path.append('..')
import crawl_util

catId_brand_map = {}
ids = []

headers = {
    'cookie': 'everywhere_tool_welcome=true; cookie2=149567e2b2700e39dbf181102ace8093; t=3f5c8aca80cc8921bb51bc3d045ea196; _tb_token_=7836e18bed1bf; _samesite_flag_=true; xlly_s=1; _m_h5_tk=50ec79008d2321b01829af658c358162_1605503375565; _m_h5_tk_enc=04bf66032e0ca7782ebf9dfbe113bafb; unb=2393890925; sn=%E5%B0%8F%E5%86%9B%E4%BA%8C%3Azhe; csg=59f48849; skt=ba78363b5c6eee68; _cc_=UtASsssmfA%3D%3D; cna=EF7KF1epo1gCAX0jZcrb8N/W; uc1=cookie14=Uoe0aDgwMULZOw%3D%3D&cookie21=VFC%2FuZ9ajQ%3D%3D; v=0; isg=BI2N2AD67t1d8ErRef9bKGBHnK8HasE8zgYPQs8SyiSTxq14l75PDQZENlqgHdn0; l=eBTmL36cOoygoTpBBOfanurza77OSIRYYuPzaNbMiOCPO61B5TsVWZ7bEqY6C3GVhs_XR38TDWZWBeYBc3xonxvtPv2ARwMmn; tfstk=crxlBog8IsNss4bD50sWBoQYFLnOwpVdse8D0nz_q6xUmo5mprzNsoGcNQxLR',
}


def brand_trademark():
    f = 'taobao_brand_trademark.csv'
    brand_trade_mark = set()
    if os.path.exists(f):
        with open(f, 'r') as r:
            r = csv.reader(r)
            next(r)
            for row in r:
                brand_trade_mark.add(row[0])
    else:
        with open(f, 'w') as w:
            w = csv.writer(w)
            w.writerow(['brand', 'nums', 'catId', '品牌名', '类目', '商标注册人', '商标注册号', '类目上的品牌状态', 'url'])
    urls = set()
    with open('urls.txt', 'r') as r:
        for url in r.readlines():
            urls.add(url.strip())
    with open(f, 'a') as w:
        w = csv.writer(w)
        with open('urls.txt', 'a') as url_w:
            with open('taobao_brand.csv', 'r') as r:
                r = csv.reader(r)
                next(r)
                cnt = 0
                for row in r:
                    cnt += 1
                    name = row[0]
                    brand = name
                    if name in brand_trade_mark or '测试' in name:
                        continue
                    catIds = json.loads(row[1])
                    find = False
                    name = name.replace('•', ' ')
                    name = name.replace('▪', ' ')
                    try:
                        name = urllib.parse.quote(name, encoding='gb18030')
                    except:
                        print('failed, %s' % name)
                    for i, catId in enumerate(catIds):
                        # if i > 2:
                        #     break
                        url = 'https://baike.taobao.com/brandCategoryApply.htm?actionType=searchAppliableBrandCategories&categoryId=%s&brandName=%s' % (
                            catId, name)
                        if url in urls:
                            continue
                        if i > 0:
                            print('%s \033[4;32;40m%s, %s/%s, %s\033[0m' % (
                                ' ' * (len(str(cnt)) + 1), brand, i + 1, len(catIds), url))
                        else:
                            print('%s, %s, %s/%s, %s' % (cnt, brand, i + 1, len(catIds), url))

                        rows = get_brand_trademark(url)

                        if rows is False:
                            return
                        for row in rows:
                            row = [brand, len(catIds), catId] + row + [url]
                            w.writerow(row)
                        if len(rows) > 0:
                            find = True
                            break
                        else:
                            url_w.write(url + '\n')
                    if not find:
                        w.writerow([brand, len(catIds), catId] + [''] * 5 + [url])


def get_brand_trademark(url):
    page = crawl_util.crawl(url, headers=headers)
    content = page.content.decode('GB18030')
    if '品牌申请' not in content:
        print('Fail, need change cookie.')
        return False
    sel = html.document_fromstring(content, parser=html.HTMLParser(encoding='GB18030'))
    trs = sel.xpath('//table/tr')
    rows = []
    for tr in trs[1:]:
        row = []
        for td in tr.getchildren()[0:5]:
            txt = td.text.strip()
            if not txt:
                txt = td.getchildren()[0].text
                txt = txt.strip() if txt else ''
            row.append(txt)
        rows.append(row)
    return rows


if __name__ == '__main__':
    brand_trademark()
