# coding=utf-8
import crawl_util
import re


crsf =''

def crawl_list(url):
    pass


def crawl_comment(url):
    pass


def crawl_detail(url):
    pass


def crawl_info(url):
    page = crawl_util.crawl(url)
    content = page.content.decode('utf-8')
    print(page.cookies)
    js = re.findall(r'href="(.*/main.[a-z0-9]+.js)"', content)
    if js:
        bearer = get_Bearer(js[0])
        print(bearer)
    gt = re.findall(r'"gt=([0-9]+);', content)
    print(gt)
    pass


def get_Bearer(url):
    page = crawl_util.crawl(url)
    print(url)
    content = page.content.decode('utf-8')
    bearer = re.findall(r'c="(AAAAAAAAAAAAAAAA[A-Za-z0-9%]+)"', content)
    return ('Bearer ' + bearer[0]) if bearer else ''


if __name__ == '__main__':
    url = 'https://twitter.com/galileocheng'
    crawl_info(url)
    pass
