# coding=utf-8

import json
import sys
import random
import re
import time
import csv
import os
import sqlite3
import threading
import traceback
import crawl_util

email = 'viking.liu@qq.com'
password = 'viking138246s'
lock = threading.Lock
headers = {
    'User-Agent': 'Instagram 35.0.0.20.96 Android (23/6.0.1; 416dpi; 1170x1872; HUAWEI; Mate 10 Pro; x86; cancro; zh_CN; 95414347)',
    'Content-Type': 'application/x-www-form-urlencoded',
    # 'X-IG-App-ID': '567067343352427'
}


def crawl_followers(userids):
    cookies = login()
    if cookies:
        for userid in userids:
            url = 'https://i.instagram.com/api/v1/friendships/%s/followers/' % userid
            print(get_content(url, cookies))


def crawl_following(userids):
    cookies = login()
    if cookies:
        for userid in userids:
            url = 'https://i.instagram.com/api/v1/friendships/%s/following/' % userid
            print(get_content(url, cookies))


def crawl_tags(tags):
    cookies = login()
    if cookies:
        for tag in tags:
            url = 'https://i.instagram.com/api/v1/feed/tag/%s/' % tag
            print(get_content(url, cookies))


def crawl_user_posts(userids):
    cookies = login()
    for userid in userids:
        url = 'https://i.instagram.com/api/v1/feed/user/%s/' % userid
        print(get_content(url, cookies))


def get_content(url, cookies, max_page=1, callback_func=None):
    print(url)
    max_id = None
    items = []
    for page in range(max_page):
        if max_id:
            url = url + '?max_id=%s' + max_id
        rsp = crawl_util.crawl(url, headers=headers, cookies=cookies)
        print(rsp.status_code)
        data = rsp.json()
        if 'items' in data:
            items += data['items']
        elif 'users' in data:
            items += data['users']

        max_id = data['next_max_id']
        if max_id is None:
            break
    return items


def crawl_user_info(userid, cookies):
    url = 'https://i.instagram.com/api/v1/users/%s/info/' % userid
    rsp = crawl_util.crawl(url, headers=headers, cookies=cookies)
    if rsp.status_code in [403, 429]:
        print('%s forbidden sleep 60s... %s' % (rsp.status_code, url))
        time.sleep(60)
    elif rsp.status_code == 404:
        return 404, {}
    if rsp and 'user' in rsp.json():
        return 200, rsp.json()['user']
    else:
        print(url, rsp)


def login():
    d = {"phone_id": "0066d903-6783-4a15-a066-3155d3e43435", "_csrftoken": "PqRg5VnrYGr6S8NrMuptqMDqmCFdYPxL",
         "username": email, "adid": "8896cc27-e0b3-40a3-a6a3-5bf1580ab45a",
         "guid": "dd0a125f-9663-485b-a54a-e457e831005a", "device_id": "android-a869eb67a6513281",
         "password": password, "login_attempt_count": "0"}
    d = json.dumps(d)
    signed_body = '122abdda46e3ec4a4a2cf45323eaee0072ee9876b6e5e05dd6813b4815571f89.' + d
    data = dict(signed_body=signed_body, ig_sig_key_version=4)
    api = 'https://i.instagram.com/api/v1/accounts/login/'
    rsp = crawl_util.crawl(api, data=data, method='post', headers=headers)
    # for cookie in rsp.cookies:
    #     if cookie.name == 'csrftoken':
    #         csrftoken = cookie.value
    #         headers['x-csrftoken'] = csrftoken
    #         break
    print('login: %s' % rsp.status_code)
    return rsp.cookies


def crawl_users(userids=None):
    cookies = login()
    if cookies:
        for i, userid in enumerate(userids):
            try:
                status, user_info = crawl_user_info(userid, cookies)
                if 'is_business' not in user_info:
                    print('status:%s fail: %s' % (status, userid))
                    continue
                user = {
                    'user_id': userid,
                    'email': user_info.get('public_email', ''),
                    'phone': user_info.get('public_phone_number', ''),
                    'code': user_info.get('public_phone_country_code', ''),
                    'name': user_info.get('username', ''),
                    'follower': user_info.get('follower_count', 0),
                    'extra': json.dumps(user_info)
                }
                print(user)
                print('%s/%s update user %s email:%s' % (i + 1, len(userids), userid, user['email']))
            except Exception as e:
                print('except fail: %s, e:%s' % (userid, e))
            time.sleep(3)


if __name__ == '__main__':
    if len(sys.argv) == 3:
        act = sys.argv[1]
        params = sys.argv[2].split(',')
        if act == 'tags':
            crawl_tags(params)
        elif act == 'users':
            crawl_users(params)
        elif act == 'follower':
            crawl_followers(params)
        elif act == 'following':
            crawl_following(params)
        elif act == 'posts':
            crawl_user_posts(params)
