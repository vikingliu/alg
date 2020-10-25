# coding=utf-8
import sys
from work.crawl import crawl_util
import re
import os
import json
import time
import csv

headers = {
    'cookie': 'x-gpf-submit-trace-id=0b5106af16032798562004195e9d93; x-gpf-render-trace-id=0b52068d16032837395571817e9c74; t=b298b9849ccccc653f45333aaad0aadc; _samesite_flag_=true; cookie2=117073fb73ef0353d1186dfcb58d625c; OUTFOX_SEARCH_USER_ID_NCOO=1763603699.7752995; thw=cn; _tb_token_=31eef8f33ebe8; enc=qLrrhwQp12KKlgqy7gKCQ0YWUEes89OsM1aXJyY6rOSc1x2pL21sgn7vt7r6d38HJ9HWvY4Avv7EMYx9CL343g%3D%3D; XSRF-TOKEN=c9f86dfb-a9ce-44cf-aadd-2a68b7980ed9; everywhere_tool_welcome=true; _bl_uid=9nkU0gC0iU9u262hLlmX34h1g0Iv; xlly_s=1; unb=2393890925; sn=%E5%B0%8F%E5%86%9B%E4%BA%8C%3Azhe; csg=e3ba4132; skt=92cfe65a3c0dc3e7; _cc_=U%2BGCWk%2F7og%3D%3D; cna=EF7KF1epo1gCAX0jZcrb8N/W; _m_h5_tk=d5d0aa95a04a1727f5c4594d6c33da9d_1603343254205; _m_h5_tk_enc=f8228924b3b776454131041307dcedb2; uc1=cookie14=Uoe0bkpV%2FUAeNw%3D%3D&cookie21=W5iHLLyFfA%3D%3D; isg=BEJCKYpkqY3Y6LXRTKwhFCq8k06kE0YtpfZ3Joxbb7Vg3-JZdqAHPP1ei9ujj77F; l=eBaTai7HOoPnI_hpBOfZnurza779sIRAguPzaNbMiOCPOvWB5PsdWZWYDn-6CnGVh6E2-3ovGkW9BeYBc_C-nxv95eL9DnMmn; tfstk=cXtGB0gTE6N5cAQHPcs6eHINumScZENAZE8HYH85AUdHMB-FiAUUz_qIt1OMDr1..',
}

ccatId_map = {}


def taobao_cat_1():
    url = 'https://item.upload.taobao.com/router/publish.htm'
    headers['referer'] = url
    page = crawl_util.crawl(url, headers=headers)
    content = page.content.decode('utf-8')
    data = re.findall(r'json:\s*(\{.*\})', content)
    with open('data/cat_1.json', 'w') as w:
        w.write(data[0])


def taobao_sub_cat():
    with open('data/cat_1.json', 'r') as r:
        data = r.read()
    data = json.loads(data)
    groups = data['components']['categorySelect']['props']['dataSource']
    for group in groups:
        print(group['groupName'])
        for child in group['children']:
            catid = child['id']
            name = child['name']
            print('--%s %s' % (catid, name))
            ccatId_map[catid] = child
            if child['id'] not in [50023724, 201173506, 124568010]:
                taobao_cat_2(catid)
            # return


def taobao_cat_2(catId):
    f = 'data/%s.json' % catId
    if os.path.exists(f):
        content = open(f).read()
    else:
        url = 'https://item.upload.taobao.com/router/asyncOpt.htm?optType=categorySelectChildren&catId=%s' % catId
        print('cate', url)
        time.sleep(0.5)
        page = crawl_util.crawl(url, headers=headers)
        content = page.content.decode('utf-8')
        if content.startswith('{"success"'):
            with open(f, 'w') as w:
                w.write(content)
        else:
            print('failed, ' + url)
            time.sleep(2)
            return None
    data = json.loads(content)
    is_leaf = False
    is_brand = False
    for item in data['data']['dataSource']:
        is_leaf = item['leaf']
        ccatId_map[item['id']] = item
        if not is_leaf:
            taobao_cat_2(item['id'])
        is_brand = item['isBrand']
        if not is_brand and is_leaf:
            # print('parent:%s child:%s leaf:%s brand:%s' %(catId, item['id'], is_leaf, is_brand))
            taobao_detail(item['id'])

    if is_leaf and is_brand:
        # print('parent:%s leaf:%s brand:%s' %(catId, is_leaf, is_brand))
        taobao_detail(catId)
        taobao_brand(catId)


def taobao_brand(catId, index=2, size=100):
    f = 'data/brand/%s.brand.txt' % catId
    res = []
    if os.path.exists(f):
        res = open(f).readlines()
        index = len(res) + 2
        if res:
            total = json.loads(res[0])['data']['total']
            if total < index * size:
                return res

    with open(f, 'a') as w:
        while True:
            url = 'https://item.upload.taobao.com/router/asyncOpt.htm?optType=taobaoBrandSelectQuery&queryType=more&catId=%s&index=%s&size=%s' % (
                catId, index, size)
            print(url)
            page = crawl_util.crawl(url, headers=headers)
            content = page.content.decode('utf-8')
            data = json.loads(content)
            total = data['data']['total']
            print('cate:%s, total:%s index:%s' % (catId, total, index))
            w.write(content + '\n')
            res.append(content)
            if total < index * size:
                break
            time.sleep(1)
            index += 1
    return res


def taobao_detail(catId):
    f = 'data/param/%s.param.json' % catId
    if os.path.exists(f):
        content = open(f).read()
    else:
        url = 'https://item.publish.taobao.com/sell/publish.htm?catId=%s&keyProps=%%7B%%7D&newRouter=1' % catId
        print('detail', url)
        page = crawl_util.crawl(url, headers=headers)
        content = page.content.decode('utf-8')
        content = re.findall(r'window.Json\s*=\s*\s*(\{.*\});', content)
        if content:
            content = content[0]
            with open(f, 'w') as w:
                w.write(content)
        else:
            print('failed, ' + url)
            time.sleep(2)
        time.sleep(0.5)
    #
    # data = json.loads(content)
    # if 'catProp' in data['components']:
    #     for item in data['components']['catProp']['props']['dataSource']:
    #         txt = [s['text'] for s in item.get('dataSource', [])]
    #         path = ccatId_map[catId]['path']
    #         path = '>'.join(path)
    #         row = [catId, ccatId_map[catId]['name'], path, item['label'], item['required'], txt]
    #         wr.writerow(row)
    #         print(row)
    #     pass
    # return data


# pw = open('taobao_cate_pro.csv', 'w')
# wr = csv.writer(pw)
# wr.writerow(['id', 'name', 'path', 'pro','required', 'values'])
if __name__ == '__main__':
    # taobao_cat_1()
    taobao_sub_cat()
    # taobao_detail('1623')
    # taobao_cat_2('1623')
    # taobao_brand('1623', 2)
