# -*- coding: UTF-8 -*-
import sys
import json
import requests
import datetime
from django.utils import timezone
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding("utf-8")


def get_videos_info():
    user_id = '1155328950'
    url = 'http://www.iqiyi.com/u/' + user_id + '/v'
    headers = {}
    headers['Host'] = 'www.iqiyi.com'
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'
    headers['Referfer'] = 'http://www.iqiyi.com/u/' + user_id
    headers['Cookie'] = '"Hm_lvt_53b7374a63c37483e5dd97d78d9bb36e=1496822614,1496823107; Hm_lpvt_53b7374a63c37483e5dd97d78d9bb36e=1496823485; QC007=https%253A%252F%252Fwww.baidu.com%252Flink%253Furl%253DVEzzNDcanCkcaqUDEB-E2JTkfS1MTfbfRrLdUFmdJ8_%2526wd%253D%2526eqid%253Dae7dc95f00012e82000000035937b54a; QC006=pat6z27t3p9wvu7o9e4chodv; QC008=1496822615.1496822615.1496822615.1; QC115=2; QC118=%7B%22color%22%3A%22FFFFFF%22%2C%22channelConfig%22%3A0%7D; QC159=%7B%22color%22%3A%22FFFFFF%22%2C%22channelConfig%22%3A0%7D; __uuid=dbd281a8-1c55-77bc-6e12-07637222dfc9; QC010=82200661; QC110=0; T00404=49a865a96ec7748739bba1d8daa6154f; T00700=EgcI67-tIRAB; QC021=%5B%7B%22key%22%3A%22insta360%22%7D%5D; QC124=1%7C0; __dfp=a016de56430a104c23871d0ff76f28f48db3019c242059fc1d74c0c43bba8f2e24@1499414619440@1496822619440"'
    headers['Connection'] = 'keep-alive'
    headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    headers['Accept-Language'] = 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'
    headers['Accept-Encoding'] = 'gzip, deflate'
    headers['Pragma'] = 'no-cache'
    headers['Cache-Control'] = 'no-cache'

    view_headers = {}
    view_headers['Host'] = 'mixer.video.iqiyi.com'
    view_headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'
    view_headers['Connection'] = 'keep-alive'
    view_headers['Accept'] = '*/*'
    view_headers['Accept-Language'] = 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'
    view_headers['Accept-Encoding'] = 'gzip, deflate'
    view_headers['Pragma'] = 'no-cache'
    view_headers['Cache-Control'] = 'no-cache'
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    result = []
    response = requests.get(url=url, headers=headers)
    page = response.text
    soup = BeautifulSoup(page, 'html.parser')
    div = soup.find('div', class_='wrap-customAuto-ht ')
    div = div.find('ul')
    li_list = div.find_all('li')
    for li in li_list:
        pic_div = li.find('div', class_='site-piclist_pic')
        info_div = li.find('div', class_='site-piclist_info')
        link_a = info_div.find('p', class_='site-piclist_info_title_twoline').find('a')
        id = li['tvid']
        # title = link_a.text
        link = link_a['href']
        thumb = pic_div.find('a').find('img')['src']
        # duration = pic_div.find('a').find('div', class_='wrapper-listTitle').find('div', class_='mod-listTitle').find('span', class_='mod-listTitle_right').text
        # temps = duration.split(':')
        # n = len(temps)
        # duration = 0
        # for i in range(n):
        #     duration += int(temps[n - i - 1]) * (60 ** (i))
        # temp = info_div.find('span', class_='playTimes_status').text[:-2]
        # published_time = datetime.datetime.strptime(temp, "%Y-%m-%d")
        # published_time = timezone.make_aware(published_time, timezone.get_current_timezone())
        view_url = 'http://mixer.video.iqiyi.com/jp/mixin/videos/' + id
        view_headers['Referer'] = link
        view_response = requests.get(url=view_url, headers=view_headers)
        view_page = view_response.text[13:]
        video_info = json.loads(view_page)
        title = video_info['name']
        view = video_info['playCount']
        duration = video_info['duration']
        like = video_info['upCount']
        dislike = video_info['downCount']
        comment = video_info['commentCount']
        timestamp = int(video_info['issueTime'] / 1000)
        published_time = datetime.datetime.fromtimestamp(timestamp)
        published_time = timezone.make_aware(published_time, timezone.get_current_timezone())
        temp = {
            'platform': u'爱奇艺',
            'video_id': id,
            'title': title,
            'published_time': published_time,
            'view': view,
            'like': like,
            'dislike': dislike,
            'comment': comment,
            'link': link,
            'thumb': thumb,
            'duration': duration,
            'date': today
        }
        result.append(temp)
    print result
    return result

if __name__ == '__main__':
    get_videos_info()
