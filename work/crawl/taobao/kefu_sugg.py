# coding=utf-8

from work.crawl import crawl_util
import urllib
import json
import time
import os
import csv

headers = {
    'Cookie': 'ucn=unszyun; _samesite_flag_=true; cookie2=1bc2d72cf718d45a796ee033ed545a94; t=44466849bbca7483d591ec21501efbcc; _tb_token_=ee31ae98331e8; _m_h5_tk=be48022d7c33630342ca504aaf4ef783_1609742441805; _m_h5_tk_enc=91a9de7da97f34996b5c1956e326a44b; xlly_s=1; unb=2393890925; sn=%E5%B0%8F%E5%86%9B%E4%BA%8C%3Azhe; csg=f39bddad; skt=937648701c93650b; _cc_=W5iHLLyFfA%3D%3D; cna=EF7KF1epo1gCAX0jZcrb8N/W; uc1=cookie14=Uoe0ZNHDCsMTHw%3D%3D&cookie21=URm48syIZQ%3D%3D; tfstk=cVcABQXtOUQxSv4-8xplCePxnV0OZSdaViZ16eRT7fllYoCOi-hn9LfwGPjYwUC..; l=eBTmL36cOoygoSuopOfwourza77OSIRAguPzaNbMiOCP9t195N4fBZ84M58pC3GVhssMR38TDWZ7BeYBcnf8egb67RtKjcDmn; isg=BHx8gRTMD_3gzjsW9nH3m64NTRwudSCfJ4EeMVb9iGdLIRyrfoXwL_KTAUlZaVj3',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'
}


def get_sugg(instanceid, keyword):
    url = 'https://everyhelp.taobao.com/inputSuggest/getInputSuggest?instanceId=%s&question=%s' % (
        instanceid, urllib.parse.quote(keyword, encoding='utf-8'))
    content = crawl_util.crawl(url, method='post', headers=headers)
    if content.status_code == 200:
        content = content.content.decode('utf-8')
        return content
    else:
        print(content.status_code, 'fail')
    return None


def get_all_sugg():
    f = 'sugg/sugg_keyword_1.txt'
    s = 'sugg/sugg_keyword_1.csv'
    keywords = set()
    if os.path.exists(s):
        with open(s, 'r') as r:
            r = csv.reader(r)
            next(r)
            for row in r:
                keywords.add(row[0])
    else:
        with open(s, 'w') as w:
            w = csv.writer(w)
            w.writerow(['keyword', 'content'])

    instanceid = 84193
    cnt = 0
    with open(s, 'a') as w:
        w = csv.writer(w)
        with open(f, 'r') as r:
            for line in r:
                cnt += 1
                keyword = line.strip()
                if keyword in keywords:
                    continue
                print(keyword, cnt)
                content = get_sugg(instanceid, keyword)
                if content:
                    w.writerow([keyword, content])
                    time.sleep(1)
                else:
                    break


if __name__ == '__main__':
    get_all_sugg()
