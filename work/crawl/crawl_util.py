# coding=utf8
import logging
import random
import re

from requests.exceptions import ProxyError

import requests
from requests.auth import HTTPDigestAuth
#
# reload(sys)
# sys.setdefaultencoding('utf-8')

h5_ua = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36'
pc_ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
app_ua = ''

session = requests.Session()

def parse_auth_url(url):
    matched = re.match('^(https?://)(.+?):(.+?)@(.+)$', url)
    if matched:
        prefix, username, password, suffix = matched.groups()
        auth = HTTPDigestAuth(username, password)
        url = prefix + suffix
        return auth, url
    return None, url


def crawl(url, h5=False, data=None, headers=None, cookies=None, auth=None, proxy=None, method='get',
          allow_redirects=True, timeout=15, clear_cookies=False):
    headers = headers if headers is not None else {}
    cookies = cookies if cookies else {}
    if 'User-Agent' not in headers and 'user-agent' not in headers:
        headers['User-Agent'] = h5_ua if h5 else pc_ua
    if auth is None:
        auth, url = parse_auth_url(url)
    proxy_start = random.randrange(1000)
    for retry in range(3):
        if clear_cookies:
            session.cookies.clear()
        if isinstance(proxy, (list, tuple)):
            current_proxy = proxy[(proxy_start + retry) % len(proxy)]
        else:
            current_proxy = proxy
        try:
            logging.info('retry=%d h5=%s proxy=%s url=%s ' % (retry, h5, current_proxy, url))
            proxies = None
            if current_proxy:
                proxies = {"http": current_proxy, 'https': current_proxy}
            if method == 'post':
                rsp = session.post(url, proxies=proxies, headers=headers, cookies=cookies, data=data, auth=auth,
                                   allow_redirects=allow_redirects,
                                   timeout=timeout)
            elif method == 'put':
                rsp = session.put(url, proxies=proxies, headers=headers, cookies=cookies, data=data, auth=auth,
                                  allow_redirects=allow_redirects,
                                  timeout=timeout)
            else:
                rsp = session.get(url, proxies=proxies, headers=headers, cookies=cookies, data=data, auth=auth,
                                  allow_redirects=allow_redirects,
                                  timeout=timeout)
            return rsp
        except ProxyError as e:
            logging.warn("Crawl while Server Error reason is %s", e.message)
            break
        except Exception as e:
            logging.exception(e)
    return None


def login(api, data, proxy=None, method='post', headers=None, cookies=None):
    rsp = crawl(api, data=data, headers=headers, cookies=cookies, allow_redirects=False, proxy=proxy, method=method)
    return rsp.cookies

