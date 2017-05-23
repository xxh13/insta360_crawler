# -*- coding: UTF-8 -*-
import sys
import json
import requests
import datetime
import re
from django.utils import timezone
reload(sys)
sys.setdefaultencoding("utf-8")


def get_videos_info():
    url = 'http://c.v.qq.com/vchannelinfo'
    headers = {}
    headers['Host'] = 'c.v.qq.com'
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'
    headers['Referfer'] = 'http://v.qq.com/vplus/insta360/videos'
    headers['Cookie'] = 'pgv_info=ssid=s6130739360; ts_last=v.qq.com/vplus/insta360/videos; pgv_pvid=9268060957; ts_uid=1707112063'
    headers['Connection'] = 'keep-alive'
    headers['Accept'] = '*/*'
    headers['Accept-Language'] = 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'
    headers['Accept-Encoding'] = 'gzip, deflate'
    params = {}
    params['otype'] = 'json'
    params['uin'] = 'a03720f017513e122a4797b4c8060361'
    params['qm'] = '1'
    params['num'] = '30'
    params['sorttype'] = '0'
    params['orderflag'] = '0'
    params['callback'] = 'jQuery19106553755452833236_1495530514227'
    params['low_login'] = '1'
    params['_'] = '1495530514234'
    page_num = 1
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    result = []
    while True:
        params['pagenum'] = str(page_num)
        response = requests.get(url=url, params=params, headers=headers)
        page = response.text
        page_num += 1
        pattern = re.compile('\{"euin":.+$', re.S)
        items = re.findall(pattern, page)
        data = json.loads(items[0][:-1])
        videos = data['videolst']
        if videos == None:
            break
        for video in videos:
            published_time = datetime.datetime.strptime(video['uploadtime'], "%Y-%m-%d")
            published_time = timezone.make_aware(published_time, timezone.get_current_timezone())
            temp = video['play_count']
            if '万' in temp:
                temp = temp[:-1]
                temp = float(temp)
                temp *= 10000
            view_count = int(temp)
            duration = video['duration']
            temps = duration.split(':')
            n = len(temps)
            duration = 0
            for i in range(n):
                duration += int(temps[n-i-1]) * (60**(i))
            view = view_count
            dislike = 0
            like = 0
            comment = 0
            link = video['url']
            title = video['title']
            duration = duration
            thumb = video['pic']
            id = video['vid']
            temp = {
                'platform': 'tencent',
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
    return result

if __name__ == '__main__':
    get_videos_info()
