# coding=utf-8

import crawl_util

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US, en;',
    'cookie': ''
}


def crawl_list(url, cookies=None):
    page = crawl_util.crawl(url, cookies=cookies)
    content = page.content.decode('utf-8')
    with open('b.html', 'w') as w:
        w.write(content)


def crawl_info(url):
    page = crawl_util.crawl(url)
    content = page.content.decode('utf-8')
    with open('a.html', 'w') as w:
        w.write(content)
    return page.cookies


if __name__ == '__main__':
    url = 'https://www.aliexpress.com/all-wholesale-products.html'

    cookies = crawl_info(url)
    # url = 'https://www.aliexpress.com/category/100003109/women-clothing.html'
    url = 'https://www.aliexpress.com/category/200001648/blouses-shirts.html'
    print(cookies)
    crawl_list(url)
