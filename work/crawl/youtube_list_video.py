# coding=utf8
# import urllib2
import re
import sys
import random
import json
import requests
import time
from bs4 import BeautifulSoup

CRAWL_URL_REPEAT_TIMES = 6
CRAWL_URL_DEPTH = 1000


def random_proxy(proxy_list):
    proxy = random.choice(proxy_list)
    proxies = {
        'http': 'http://' + proxy,
        'https': 'http://' + proxy,
    }
    return proxies


def crawl_list(list_type, proxy_list, ctp, con, page, max_page=-1, depth=1, more_info=False):
    videos = []
    if page > max_page and max_page > 0:
        return videos

    url = 'https://m.youtube.com/%s?action_continuation=1&ajax=1&ctoken=%s&itct=%s&layout=mobile&tsp=1&utcoffset=480' % (
        list_type, con, ctp)
    for i in range(CRAWL_URL_REPEAT_TIMES):
        try:
            proxy = random.choice(proxy_list)
            content = crawl_util.crawl(url, yt_h5=True, proxy=proxy)
            if content:
                break
            if content is None:
                return None
        except Exception as e:
            pass
    content = content.replace(")]}'", '')
    # content = content.decode('unicode_escape')
    content = content.replace('\\U', '\\\\U')
    if content:
        data = json.loads(content)
        contents = data['content']['continuation_contents']
        if page == 1:
            contents = contents['contents'][0]
            continuations = contents['continuations']
        else:
            if 'continuations' not in contents:
                return videos
            continuations = contents['continuations']
        items = contents['contents']
        for item in items:
            if 'endpoint' in item:
                url = item['endpoint']['url']
                if more_info:
                    info = dict(url='https://www.youtube.com' + url,
                                title=item['title']['runs'][0]['text'],
                                thumb_url='https://www.youtube.com' + item['thumbnail_info']['url'],
                                playlist_id=item['playlist_id'])
                    videos.append(info)
                else:
                    videos.append('https://www.youtube.com' + url)
        for continuation in continuations:
            ctp = continuation['click_tracking_params']
            con = continuation['continuation']
            item_type = continuation['item_type']
            if item_type == 'next_continuation_data' and depth + 1 < CRAWL_URL_DEPTH:
                new_videos = crawl_list(list_type, proxy_list, ctp, con, page + 1, max_page, depth + 1, more_info)
                if new_videos is None:
                    return None
                videos += new_videos
    return videos


def crawl_user(user, proxy_list, max_page=-1):
    url = 'https://m.youtube.com/%s/videos?ajax=1&layout=mobile&tsp=1&utcoffset=480' % user
    for _ in range(CRAWL_URL_REPEAT_TIMES):
        try:
            proxy = random.choice(proxy_list)
            content = crawl_util.crawl(url, yt_h5=True, proxy=proxy)
            if content:
                break
            if content is None:
                return None
        except Exception as e:
            pass
    else:
        return None
    content = content.replace(")]}'", '')
    content = content.replace('\\U', '\\\\U')
    if content:
        data = json.loads(content)
        tabs = data['content']['tab_settings']['available_tabs']
        author = data['content']['header']['title']
        channel_url = data['content']['header']['channel_url']
        avatar = data['content']['header']['avatar']['url']
        for tab in tabs:
            if tab['title'] == 'Home' and 'endpoint' in tab:
                user = tab['endpoint']['url']
                email = user.split('/')[2] + '@bytedance.com'

            if tab['title'] == 'Videos' and 'sub_menu' in tab['content']:
                items = tab['content']['sub_menu']['sort_filter_sub_menu_items']
                for item in items:
                    if item['title'] != 'Date added (newest)':
                        continue
                    ctp = item['continuation']['click_tracking_params']
                    con = item['continuation']['continuation']
                    videos = crawl_list(user, proxy_list, ctp, con, 1, max_page, 1)
                    if videos is None:
                        return None
                    return dict(author=author, avatar=avatar, videos=videos, email=email)
    return {}


def crawl_youtube_url(url, latest=True, proxy_list=['10.100.4.155:3128']):
    query = ""
    match_user_or_channel = r'(?:https://|http://)?(?:www.)?(?:youtube.com){1}/(user|channel){1}/([a-zA-Z0-9_-]{1,})'
    match_only_user = r'(?:https://|http://)?(?:www.)?(?:youtube.com){1}/([a-zA-Z0-9_-]{1,})'
    result = re.match(match_user_or_channel, url)
    if result:
        result_t = result.groups()
        query = result_t[0] + '/' + result_t[1]
    else:
        result = re.match(match_only_user, url)
        if result:
            query = result.groups()[0]
    if query:
        max_page = 1 if latest else -1
        return crawl_user(query, proxy_list, max_page)


# 通过访问 m.youtube.com 接口取youtube视频list失败率飙升，改成新接口
def crawl_youtube_url2(url, latest=True, proxy_list=['10.100.4.155:3128']):
    def get_video_detail(soup):
        videos_array = []
        for td in soup.find_all(class_="yt-lockup-content"):
            try:
                video_dict = {}
                video_detail = td.find(
                    class_="yt-uix-sessionlink yt-uix-tile-link spf-link yt-ui-ellipsis yt-ui-ellipsis-2")
                if not video_detail:
                    continue
                video_dict["title"] = video_detail.get("title", "").replace("\r", "").replace("\n", "").replace("\'",
                                                                                                                "")
                video_dict["date"] = td.find_all("li")[-1].get_text()
                video_dict["path"] = video_detail.get("href", "").split("=")[1]  # watch=xxx
                video_dict["view"] = -1
                if len(td.find_all("li")) > 0 and len(re.findall(r'\d+', td.find_all("li")[0].get_text())) > 0:
                    video_dict["view"] = int(re.findall(r'\d+', td.find_all("li")[0].get_text())[0])
                videos_array.append(video_dict)
            except Exception as e:
                pass
        return videos_array

    start_time = time.time()

    all_videos_array = []
    try:
        response = requests.get(url, proxies=random_proxy(proxy_list))
        soup = BeautifulSoup(response.text.encode("utf8"))
        part_video_array = get_video_detail(soup)

        all_videos_array.extend(part_video_array)
        load_more = re.findall('data-uix-load-more-href=".*?"', response.text)
        if len(load_more) >= 1:
            next_page_url = "https://www.youtube.com{}".format(load_more[0][25: -1])
            keep_fetching = True
            while not latest and next_page_url and keep_fetching:
                # 30分钟还没有抓完，强制停止
                if time.time() - start_time > 1800:
                    break

                response = requests.get(next_page_url, proxies=random_proxy(proxy_list))
                res_dict = json.loads(response.text)
                soup = BeautifulSoup(res_dict["content_html"])
                more_videos_array = get_video_detail(soup)
                keep_fetching = bool(more_videos_array)
                all_videos_array.extend(more_videos_array)

                if not res_dict.has_key("load_more_widget_html") or res_dict["load_more_widget_html"] == "":
                    break
                load_more = re.findall('data-uix-load-more-href=".*?"', res_dict["load_more_widget_html"])
                if len(load_more) < 1:
                    break
                next_page_url = "https://www.youtube.com{}".format(load_more[0][25: -1])
    except Exception as e:
        pass

    ytb_video_prefix = 'https://www.youtube.com/watch?v='
    videos = [ytb_video_prefix + video_detail.get('path') for video_detail in all_videos_array if
              video_detail and video_detail.get('path')]
    author = ''
    avatar = ''
    email = ''
    return dict(author=author, avatar=avatar, videos=list(set(videos)), email=email)


def play_list(l, proxy_list, max_page):
    url = 'https://m.youtube.com/playlist?ajax=1&layout=mobile&list=%s&tsp=1&utcoffset=480' % l
    proxy = random.choice(proxy_list)
    content = crawl_util.crawl(url, yt_h5=True, proxy=proxy)
    content = content.replace(")]}'", '')
    content = content.replace('\\U', '\\\\U')
    videos = []
    if content:
        data = json.loads(content)
        data = data['content']['section_list']['contents'][0]['contents'][0]
        items = data['contents']
        for item in items:
            if 'endpoint' in item:
                url = item['endpoint']['url']
                videos.append('https://www.youtube.com' + url)
        for continuation in data['continuations']:
            ctp = continuation['click_tracking_params']
            con = continuation['continuation']
            item_type = continuation['item_type']
            if item_type == 'next_continuation_data':
                videos += crawl_list('playlist', proxy_list, ctp, con, 2, max_page)
    return videos


def crawl_youtube_plays(url, latest=True, proxy_list=['10.100.4.155:3128']):
    query = ""
    match_user_or_channel = r'(?:https://|http://)?(?:www.)?(?:youtube.com){1}/(user|channel){1}/([a-zA-Z0-9_-]{1,})'
    match_only_user = r'(?:https://|http://)?(?:www.)?(?:youtube.com){1}/([a-zA-Z0-9_-]{1,})'
    result = re.match(match_user_or_channel, url)
    if result:
        result_t = result.groups()
        query = result_t[0] + '/' + result_t[1]
    else:
        result = re.match(match_only_user, url)
        if result:
            query = result.groups()[0]
    if query:
        max_page = 1 if latest else -1
        return crawl_plays(query, proxy_list, max_page)


def crawl_plays(user, proxy_list, max_page):
    url = 'https://m.youtube.com/%s/playlists?ajax=1&layout=mobile&tsp=1&utcoffset=480' % user
    proxy = random.choice(proxy_list)
    content = crawl_util.crawl(url, yt_h5=True, proxy=proxy)
    content = content.replace(")]}'", '')
    content = content.replace('\\U', '\\\\U')
    videos = []
    if content:
        data = json.loads(content)
        data = data['content']['tab_settings']['available_tabs'][2]['content']['contents'][0]
        items = data['contents']
        for item in items:
            if 'endpoint' in item:
                url = item['endpoint']['url']
                info = dict(url='https://www.youtube.com' + url,
                            title=item['title']['runs'][0]['text'],
                            thumb_url='https://www.youtube.com' + item['thumbnail_info']['url'],
                            playlist_id=item['playlist_id'])
                videos.append(info)
        for continuation in data['continuations']:
            ctp = continuation['click_tracking_params']
            con = continuation['continuation']
            item_type = continuation['item_type']
            if item_type == 'next_continuation_data':
                videos += crawl_list(user, proxy_list, ctp, con, 2, max_page, more_info=True)
    return videos


def search(keyword, proxy_list, max_page):
    url = 'https://m.youtube.com/results?ajax=1&layout=mobile&search_query=%s&tsp=1&utcoffset=480' % keyword
    proxy = random.choice(proxy_list)
    content = crawl_util.crawl(url, yt_h5=True, proxy=proxy)
    content = content.replace(")]}'", '')
    content = content.replace('\\U', '\\\\U')
    if content:
        data = json.loads(content)
        data = data['content']
        videos = []
        if 'search_results' not in data:
            return videos
        items = data['search_results']['contents']
        for item in items:
            if 'endpoint' in item:
                url = item['endpoint']['url']
                videos.append('https://www.youtube.com' + url)

        for continuation in data['search_results']['continuations']:
            ctp = continuation['click_tracking_params']
            con = continuation['continuation']
            item_type = continuation['item_type']
            if item_type == 'next_continuation_data':
                videos += crawl_list('results', ctp, con, 2, max_page)
        rst = []
        for url in videos:
            if url.find('youtube.com/playlist') > -1:
                l = url.split('?')[-1].replace('list=', '')
                rst += play_list(l, max_page)
            elif url.find('youtube.com/channel') > -1:
                user = url.split('.com/')[-1]
                user_info = crawl_user(user, max_page)
                if user_info:
                    rst += user_info['videos']
            elif url.find('youtube.com/watch') > -1:
                rst.append(url)
            else:
                print(url)
        videos = rst

        return list(set(videos))


if __name__ == '__main__':
    # video_info = crawl_user(sys.argv[1], 2)
    # video_info = crawl_youtube_url(sys.argv[1], False)
    proxy_list = ['10.100.4.155:3128', '10.100.4.156:3128', '10.100.4.157:3128']

    video_info = crawl_youtube_url2(sys.argv[1], False, proxy_list)
    if video_info:
        print(len(video_info['videos']))
