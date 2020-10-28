# coding=utf-8
import json
import re
from lxml import html
from work.crawl import crawl_util
import os
import csv
import time


def get_cate():
    f = 'cate_urls.txt'
    if os.path.exists(f):
        urls = [url.strip() for url in open(f).readlines()]
        return set(urls)

    txt = open('jd_cate.json').read()
    data = json.loads(txt)
    urls = set()
    for cat_1 in data['data']:
        for cat_2 in cat_1['s'][0]['s']:
            for cat_3 in cat_2['s']:
                values = cat_3['n'].split('|')
                cat_3_url = values[0].split('&')[0]
                catid = re.findall('^(\d+-\d+)', cat_3_url)
                if catid:
                    cat_3_url = 'list.jd.com/list.html?cat=' + cat_3_url.replace('-', ',')
                cat_3_url = 'https://' + cat_3_url
                if 'cat=' in cat_3_url or 'sub=' in cat_3_url or 'tid=' in cat_3_url or 'search.jd.com' in cat_3_url:
                    urls.add(cat_3_url)

    txt = open('jd_Industrial_cate.json').read()
    data = json.loads(txt)
    for cat_1 in data['categoryDownLabel']:
        for cat_2 in cat_1['items']:
            for cat_3 in cat_2['items']:
                cat_3_url = cat_3['url'].split('&')[0]
                if not cat_3_url.startswith('https:'):
                    cat_3_url = 'https:' + cat_3_url
                if 'i-search' in cat_3_url:
                    cat_3_url += '&enc=utf-8'
                urls.add(cat_3_url)
    with open(f, 'w') as w:
        for url in urls:
            w.write(url + '\n')
    return urls


def get_cate_pro(url):
    domain = url.split('jd.com')[0] + 'jd.com'
    page = crawl_util.crawl(url)
    content = page.content.decode('utf-8')
    sel = html.document_fromstring(content, parser=html.HTMLParser(encoding='utf-8'))
    cat_3s = sel.xpath('//ul[@class="menu-drop-list"]/li/a')
    urls = []
    for cat_3 in cat_3s:
        cat_3_url = cat_3.attrib['href']
        if 'cat=' in cat_3_url or 'sub=' in cat_3_url or 'tid=' in cat_3_url or 'search' in cat_3_url:
            urls.append(domain + cat_3_url)
    pros = sel.xpath('//div[@id="J_selector"]/div')
    name_values = []
    if pros:
        for pro in pros:
            rst = func_pro(pro)
            name_values += rst
    other_exts = re.findall(r'other_exts\s*=\s*(.*?\]);', content)
    if other_exts:
        other_exts = json.loads(other_exts[0])
        for ext in other_exts:
            if 'attr_infos' in ext:
                if ext['attr_infos']:
                    values = [info['name'] for info in ext['attr_infos']]
                else:
                    values = ext['value_name'].split(';')
                rst.append((ext['name'], values))
    cat_1 = sel.xpath('//div[@class="crumbs-nav-item one-level"]/a')
    cat_1 = cat_1[0].text if cat_1 else ''
    cat_2_3 = sel.xpath('//span[@class="curr"]')
    cat_2_3 = [span.text for span in cat_2_3]
    path = [cat_1] + cat_2_3
    cat_name = path[-1]
    path = '>'.join(path)
    rows = []
    for name, values in name_values:
        row = [url, cat_name, path, name, values]
        rows.append(row)
    return urls, rows


def func_pro(pro):
    name = pro.xpath('.//div[@class="sl-key"]/span')
    if not name:
        name = pro.xpath('.//div[@class="sl-key"]/strong')
    if name:
        name = name[0].text.replace(':', '').replace('：', '')
    else:
        return []
    if name == '品牌':
        values = func_brand(pro)
    elif name == '高级选项':
        return func_more(pro)
    else:
        items = pro.xpath('.//ul[@class="J_valueList"]/li/a')
        if items and items[0].getchildren()[0].tail:
            values = [item.getchildren()[0].tail.strip() for item in items]
        else:
            values = [item.attrib['title'] for item in items]
    return [(name, values)]


def func_brand(pro):
    brands = pro.xpath('.//div/ul[@class="J_valueList v-fixed"]/li/a')
    if not brands:
        brands = pro.xpath('.//div/ul[@class="J_valueList "]/li/a')
    if not brands:
        brands = pro.xpath('.//div/ul[@class="J_valueList"]/li/a')
    return [brand.attrib.get('title', '') for brand in brands]


def func_more(pro):
    items = pro.xpath('.//a[@class="trig-item"]/span')
    names = [item.text for item in items]
    values_list = pro.xpath('.//div[@class="sl-tab-cont-item"]')
    rst = []
    for i, v_list in enumerate(values_list):
        values = v_list.xpath('.//ul/li/a')
        values = [value.getchildren()[0].tail for value in values]
        rst.append((names[i], values))
    return rst


def get_all_pro():
    urls = get_cate()
    f = 'jd_cate_pro.csv'
    url_pros = set()
    if os.path.exists(f):
        with open(f, 'r') as r:
            r = csv.reader(r)
            next(r)
            for row in r:
                url_pros.add(row[0])
    else:
        with open(f, 'a') as w:
            w = csv.writer(w)
            w.writerow(['url', 'name', 'path', 'pro', 'values'])
    print(len(url_pros))
    with open('cate_urls.txt', 'a') as url_w:
        with open(f, 'a') as w:
            w = csv.writer(w)
            need_crawl_urls = list(urls)
            cnt = 0
            for url in need_crawl_urls:
                cnt += 1
                if url in url_pros:
                    continue
                url_pros.add(url)
                print(url)
                new_urls, rows = get_cate_pro(url)
                for new_url in new_urls:
                    if new_url not in urls:
                        print('record new url', new_url)
                        need_crawl_urls.append(new_url)
                        urls.add(new_url)
                        # save the new url to file
                        url_w.write(new_url + '\n')
                print('%s/%s, pros: %s, url:%s' % (cnt, len(need_crawl_urls), len(rows), url))
                w.writerows(rows)
                time.sleep(0.5)


if __name__ == '__main__':
    get_all_pro()
