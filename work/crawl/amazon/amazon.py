# coding=utf-8
from lxml import html
import time
import sys
sys.path.append('..')
import crawl_util

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US, en;',
}


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


def get_all_list():
    with open('cat4_list.txt', 'r') as r:
        for url in r.readlines():
            url = url.strip()

            if url.find('https') >= 0:
                print(url)
                get_list(url)
                time.sleep(5)

def get_list(url):
    page = crawl_util.crawl(url, headers=headers)
    content = page.content.decode('utf-8')
    sel = html.document_fromstring(content, parser=html.HTMLParser(encoding='utf-8'))
    products = sel.xpath('//div[@class="sg-col-inner"]')
    if not products:
        products = sel.xpath('//div[@class="s-item-container"]')
    if products:
        print(len(products))
        next_page = sel.xpath('//li[@class="a-last"]/a')
        if not next_page:
            next_page = sel.xpath('//a[@id="pagnNextLink"]')
        if next_page:
            href = next_page[0].attrib['href']
            next_url = 'https://www.amazon.co.uk' + href
            print('next page', next_url)

    with open('../b.html', 'w') as w:
        w.write(content)


def crawl_cate(url):
    page = crawl_util.crawl(url, headers=headers)
    content = page.content.decode('utf-8')
    get_cats(content)


if __name__ == '__main__':
    get_all_list()

