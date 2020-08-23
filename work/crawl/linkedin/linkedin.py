# coding=utf-8
import csv
import json
from lxml import html
import sys

sys.path.append('..')
import crawl_util

cookie = open('cookie.txt').read().strip()
headers = {
    'Cookie': cookie,
}


def crawl(url, referer=''):
    headers['referer'] = referer
    rsp = crawl_util.crawl(url, headers=headers)
    return rsp.content


def crawl_linkedin(link, f_name):
    page = 1
    with open(f_name, 'wb') as w:
        w = csv.writer(w)
        w.writerow(['name', 'location', 'occupation', 'link'])
        while True:
            url = link + '&page=%s' % page
            # url = 'https://www.linkedin.com/search/results/people/?facetCurrentCompany=%s&facetGeoRegion=%s&keywords=%s&origin=FACETED_SEARCH&page=%s' % (facetCurrentCompany, facetGeoRegion, keywords, page)
            print url
            content = crawl(url)
            sel = html.fromstring(content)
            codes = sel.xpath('//code')
            for code in codes:
                if code.text and 'totalResultCount' in code.text:
                    data = json.loads(code.text)
                    break
            els = data['data']['elements']
            if len(els) == 0:
                break
            els = els[1] if len(els) > 1 else els[0]
            if 'elements' not in els:
                break
            els = els['elements']
            for item in els:
                uid = item.get('publicIdentifier', '')
                profile = '' if uid == '' else 'https://www.linkedin.com/in/' + uid
                row = [get_text(item, 'title'), get_text(item, 'subline'), get_text(item, 'headline'),
                       profile.encode('utf-8')]
                w.writerow(row)

            total = data['data']['paging']['total']
            max_page = total / 10 + 1
            page += 1
            if page > max_page:
                break


def get_text(item, key):
    return item.get(key, {}).get('text', '').encode('utf-8')


if __name__ == '__main__':
    f = open('conf.txt')
    params = {}
    for line in f.readlines():
        line = line.strip()
        if line.startswith('#') or ':' not in line:
            continue
        key, value = line.split(':', 1)
        params[key] = value.strip()
    print params
    crawl_linkedin(params['link'], params['file'])
