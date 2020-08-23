# coding=utf-8

import json
import re
import urllib
import requests
import time


def crawl(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36'}
    rsp = requests.get(url, headers=headers)
    return rsp.content


code_cache = {}


def cache(func):
    def fun(*args, **kwargs):
        now = int(time.time())
        js = args[0]
        if js in code_cache:
            _code, t = code_cache[js]
            if now - t < 3600:
                return _code
        _code = func(*args, **kwargs)
        code_cache[js] = (_code, now)
        return _code

    return fun


def tr_js(code):
    code = re.sub(r'function', r'def', code)
    code = re.sub(r'(\W)(as|if|in|is|or)\(', r'\1_\2(', code)
    code = re.sub(r'\$', '_dollar', code)
    code = re.sub(r'\{', r':\n\t', code)
    code = re.sub(r'\}', r'\n', code)
    code = re.sub(r'var\s+', r'', code)
    code = re.sub(r'(\w+).join\(""\)', r'"".join(\1)', code)
    code = re.sub(r'(\w+).length', r'len(\1)', code)
    code = re.sub(r'(\w+).slice\((\w+)\)', r'\1[\2:]', code)
    code = re.sub(r'(\w+).splice\((\w+),(\w+)\)', r'del \1[\2:\2+\3]', code)
    code = re.sub(r'(\w+).split\(""\)', r'list(\1)', code)
    return code


# @cache
def decipher(js, s):
    _code = get_code(js)
    exec _code
    return locals()['sig']


@cache
def get_code(js):
    # find this f.url, f.sp, f.s in base.js
    js = crawl(js)
    js = js.replace('\n', ' ')
    # \w+=function\(\w+\)\{.*?split\(""\).*?join\(""\)\}
    # function \w+\(\w+\)\{.*?split\(""\).*?join\(""\)\}
    f1 = match(js, r'=\s*(\w+)\(decodeURIComponent')
    # f1 = match(js, r'\W(\w+)=function\(\w+\)\{\w+=\w+\.split\(""\)[^\{]+join\(""\)\}') or \
    #    match(js, r'function (\w+)\(\w+\)\{\w+=\w+\.split\(""\)[^\{]+join\(""\)\}')

    f1def = match(js, r'function %s(\(\w+\)\{[^\{]+\})' % re.escape(f1)) or \
            match(js, r'\W%s=function(\(\w+\)\{[^\{]+\})' % re.escape(f1))
    f1def = re.sub(r'([$\w]+\.)([$\w]+\(\w+,\d+\))', r'\2', f1def)
    f1def = 'function %s%s' % (f1, f1def)
    _code = tr_js(f1def)
    f2s = set(re.findall(r'([$\w]+)\(\w+,\d+\)', f1def))
    for f2 in f2s:
        f2e = re.escape(f2)
        f2def = re.search(r'[^$\w]%s:function\((\w+,\w+)\)(\{[^\{\}]+\})' % f2e, js)
        if f2def:
            f2def = 'function {}({}){}'.format(f2e, f2def.group(1), f2def.group(2))
        else:
            f2def = re.search(r'[^$\w]%s:function\((\w+)\)(\{[^\{\}]+\})' % f2e, js)
            f2def = 'function {}({},b){}'.format(f2e, f2def.group(1), f2def.group(2))
        f2 = re.sub(r'(\W)(as|if|in|is|or)\(', r'\1_\2(', f2)
        f2 = re.sub(r'\$', '_dollar', f2)
        _code += 'global %s\n' % f2 + tr_js(f2def)

    f1 = re.sub(r'(as|if|in|is|or)', r'_\1', f1)
    f1 = re.sub(r'\$', '_dollar', f1)
    _code += 'sig=%s(s)' % f1
    return _code


def match(text, *patterns):
    if len(patterns) == 1:
        pattern = patterns[0]
        m = re.search(pattern, text)
        if m:
            return m.group(1)
        else:
            return None
    else:
        ret = []
        for pattern in patterns:
            m = re.search(pattern, text)
            if m:
                ret.append(m.group(1))
        return ret


def get_youtube(url, proxy=None):
    # url = url.replace('www.youtube.com', 'm.youtube.com')
    print url
    page = crawl(url)
    meta = re.findall(r'ytplayer\.config\s*=\s*(\{".*?\}\});', page)
    js = re.findall(r'src="([^"]+base.js)"', page)
    js = ('https://www.youtube.com' + js[0]) if js else ''

    if meta:
        meta = json.loads(meta[0])
        play_data = meta['args']['player_response']
        play_data = json.loads(play_data)

        # formats = play_data['streamingData']['adaptiveFormats']
        formats = play_data['streamingData']['formats']
        urls = []
        for f in formats:
            if 'cipher' in f or 'signatureCipher' in f:
                cipher = f.get('cipher', '') or f.get('signatureCipher', '')
                params = cipher.split('&')
                params = {p.split('=')[0]: p.split('=')[1] for p in params}
                sig = urllib.unquote(decipher(js, urllib.unquote(params['s'])))
                # sig = urllib.unquote(decipher_1(urllib.unquote(params['s'])))
                url = urllib.unquote(params['url']) + '&sig=' + sig
                urls.append(url)
            else:
                urls.append(f['url'])

        return urls
    return []


if __name__ == '__main__':
    # urls = get_youtube('https://www.youtube.com/watch?v=6lXVtCjJrz0')
    # url = 'https://www.youtube.com/watch?v=6lXVtCjJrz0'
    url = 'https://www.youtube.com/watch?v=G4oUeS2ziuw'
    # url = 'https://www.youtube.com/watch?v=iuHnR3Leyqw'
    urls = get_youtube(url)
    for url in urls:
        print url
