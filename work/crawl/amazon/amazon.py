# coding=utf-8
from lxml import html
import time
import sys
import os
import csv
import hashlib
from collections import defaultdict

sys.path.append('..')
import crawl_util

proxy = 'helo_crm_liuhongxia.mandy:zPtTv2LwbznHLcTc@10.124.155.190:8080'
# proxy = ''

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US, en;q=0.9',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15',
    # 'cookie': 'csm-hit=tb:s-GCSNVP4GHMN3MMRDTKH9|1600079633345&t:1600079634309&adb:adblk_no'
}
amazon_catids = defaultdict(int)


def get_product1(products, category, total, cate_page):
    items = []
    for product in products:
        item = [category]
        title = product.xpath('.//a/h2')
        item.append(title[0].text if title else '')
        comment = product.xpath('.//div[@class="a-row a-spacing-top-mini a-spacing-none"]/a')
        item.append(comment[0].text if comment else '')
        star = product.xpath('.//i/span[@class="a-icon-alt"]')
        item.append(star[0].text if star else '')
        price = product.xpath('.//span[@class="a-size-base a-color-price s-price a-text-bold"]')
        if not price:
            price = product.xpath('.//span[@class="a-color-price"]')
        item.append(price[0].text if price else '')
        best = product.xpath('.//span/span[@class="a-badge-text"]')
        item.append(best[0].text if best else '')
        img = product.xpath('.//a[@class="a-link-normal a-text-normal"]/img')
        item.append(img[0].attrib['src'] if img else '')
        detail = title[0].getparent() if title else None
        if detail is not None:
            item.append(detail.attrib['href'])
            item.append(total)
            item.append(cate_page)
            items.append(item)
    return items


def get_product2(products, category, total, cate_page):
    items = []
    for product in products:
        item = [category]
        title = product.xpath('.//span[@class="a-size-medium a-color-base a-text-normal"]')
        if not title:
            title = product.xpath('.//span[@class="a-size-base-plus a-color-base a-text-normal"]')
        item.append(title[0].text if title else '')
        comment = product.xpath('.//span[@class="a-size-base"]')
        item.append(comment[0].text if comment else '')
        star = product.xpath('.//i/span[@class="a-icon-alt"]')
        item.append(star[0].text if star else '')
        price = product.xpath('.//span[@class="a-price-whole"]')

        item.append(price[0].text if price else '')
        best = product.xpath('.//span/span[@class="a-badge-text"]')
        item.append(best[0].text if best else '')
        img = product.xpath('.//img[@class="s-image"]')
        item.append(img[0].attrib['src'] if img else '')
        detail = title[0].getparent() if title else None
        if detail is not None:
            item.append('https://www.amazon.co.uk' + detail.attrib['href'])
            item.append(total)
            item.append(cate_page)
            items.append(item)
    return items


def get_products(sel, category='', total='', cate_page=''):
    p_xpath = {
        '//div[@class="s-item-container"]': get_product1,
        '//div[@class="a-section a-spacing-medium"]': get_product2,
        '//div[@class="sg-col-4-of-24 sg-col-4-of-12 sg-col-4-of-36 s-result-item s-asin sg-col-4-of-28 sg-col-4-of-16 sg-col sg-col-4-of-20 sg-col-4-of-32"]': get_product2,
    }
    for xpath, func in p_xpath.items():
        products = sel.xpath(xpath)
        if products:
            return func(products, category, total, cate_page)


def get_next_page(sel):
    next_xpath = ['//li[@class="a-last"]/a', '//a[@id="pagnNextLink"]']
    for xpath in next_xpath:
        next_page = sel.xpath(xpath)
        if next_page:
            href = next_page[0].attrib['href']
            next_url = 'https://www.amazon.co.uk' + href
            return next_url
    return ''


def crawl_list(url, cate_page):
    page = crawl_util.crawl(url, headers=headers, proxy=proxy)
    if page is None or page.status_code != 200:
        succ = True
        if page:
            print('status code %s' % page.status_code)
            succ = False2

        return None, 0, succ
    content = page.content.decode('utf-8')
    sel = html.document_fromstring(content, parser=html.HTMLParser(encoding='utf-8'))
    total = sel.xpath('//span[@id="s-result-count"]')
    if not total:
        total = sel.xpath('//div[@class="a-section a-spacing-small a-spacing-top-small"]/span[1]')
    total = total[0].text if total else '0'
    if total:
        total = total.replace('results for', '')
        total = total.replace(',', '')
        total = total.split('over')[-1].strip()
        total = total.split('of')[-1].strip()
    else:
        total = '0'
    categories = sel.xpath('//span[@id="s-result-count"]/span')
    cates = []
    if not categories:
        categories = sel.xpath('//div[@class="a-section a-spacing-small a-spacing-top-small"]/a/span')
        for cate in categories:
            cates.append(cate.text)
        cat3 = sel.xpath(
            '//div[@class="a-section a-spacing-small a-spacing-top-small"]/span[@class="a-color-state a-text-bold"]')
        if cat3:
            cates.append(cat3[0].text)
    else:
        for cate in categories[0].getchildren():
            cates.append(cate.text)
    category = ':'.join(cates)
    products = get_products(sel, category, total, cate_page)
    find = len(products) if products else 0
    print(category, cate_page, total, find)
    succ = True
    if content.find('Enter the characters you see below') > 0:
        print('failed: ' + url)
        succ = False
    return products, int(total), succ


def crawl_all_list():
    with open('cat4_list.txt', 'r') as r:
        lines = r.readlines()

    with open('amazon.csv', 'a') as w:
        w = csv.writer(w)

        for i, url in enumerate(lines):
            url = url.strip()
            cate_id = hashlib.md5(url.encode('utf-8')).hexdigest()
            if url.startswith('https'):
                has_crawled = 0
                for page in range(1, 100):
                    link = url + ('&page=%s' % page)
                    cate_page = cate_id + '_%s' % page
                    if cate_page in amazon_catids:
                        print('find %s %s' % (cate_page, amazon_catids[cate_page]))
                        has_crawled += amazon_catids[cate_page]
                        continue
                    if has_crawled >= 240:
                        break
                    print('%s/%s' % (i + 1, len(lines)), cate_page, link)
                    products, total, succ = crawl_list(link, cate_page)
                    if products:
                        w.writerows(products)
                        has_crawled += len(products)
                    elif not succ:
                        return
                    if  has_crawled >= total:
                        break

                    time.sleep(5)


def crawl_cate(url):
    page = crawl_util.crawl(url, headers=headers)
    content = page.content.decode('utf-8')
    get_cats(content)


def get_cats(page):
    sel = html.document_fromstring(page, parser=html.HTMLParser(encoding='utf-8'))
    cat1_all = sel.xpath('//ul')
    for cat1 in cat1_all:
        cat2_all = cat1.xpath('.//li')
        for cat2 in cat2_all:
            children = cat2.getchildren()
            if children:
                child = children[0]
                if child.tag == 'a' and child.text:
                    text = child.text
                    href = child.attrib['href']
                    if href.find('browse.html') > 0:
                        url = 'https://www.amazon.co.uk' + href
                        print(text, url)


def read_csv():
    cnt = 0
    if os.path.exists('amazon.csv'):
        with open('amazon.csv', 'r') as r:
            r = csv.reader(r)
            for product in r:
                cnt += 1
                amazon_catids[product[-1]] += 1
        print('already crawl products: %s, pages: %s' % (cnt, len(amazon_catids)))
    else:
        with open('amazon.csv', 'w') as w:
            w = csv.writer(w)
            w.writerow(['category', 'title', 'comment', 'starRating', 'price', 'best seller', 'image', 'detail', 'sku',
                        'catid_page'])


if __name__ == '__main__':
    read_csv()
    crawl_all_list()
    # url = 'https://www.amazon.co.uk/Womens-Dungarees/b/ref=amb_link_4?ie=UTF8&node=1731466031&pf_rd_m=A3P5ROKL5A1OLE&pf_rd_s=merchandised-search-left-13&pf_rd_r=3N1B6J3Y78CH362EN7HZ&pf_rd_r=3N1B6J3Y78CH362EN7HZ&pf_rd_t=101&pf_rd_p=207e4807-cac2-4a42-88f0-8f0cfd0d5c4d&pf_rd_p=207e4807-cac2-4a42-88f0-8f0cfd0d5c4d&pf_rd_i=1731296031&page=4'
    # url = 'https://www.amazon.co.uk/s?bbn=1730929031&rh=n%3A83450031%2Cn%3A%2183451031%2Cn%3A1730929031%2Cn%3A1730993031&dc&page=2&fst=as%3Aoff&qid=1599727609&rnid=1730929031&ref=lp_1730929031_nr_n_1'
    # print(crawl_list(url, ''))
