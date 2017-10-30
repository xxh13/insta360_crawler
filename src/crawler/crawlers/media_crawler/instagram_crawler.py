# -*- coding: UTF-8 -*-
'''
stack overflow里找到的官方接口，官方文档中没有
最近一周动态的评论、点赞总和
'''
import urllib2
import json
import datetime
import time
import requests
import re


def get_by_api():
    username = 'insta360official'
    url = 'https://www.instagram.com/' + username + '/media/'
    now = time.mktime(datetime.date.today().timetuple())
    week_ago = now - (3600 * 24 * 7)
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    like_total = 0
    comment_total = 0
    view_total = 0
    request = urllib2.Request(url = url)
    response = urllib2.urlopen(request)
    page = response.read()
    jsonData = json.loads(page, encoding="utf-8")
    data = jsonData['items']
    for item in data:
        temp = int(item['created_time'])
        if temp >= week_ago:
            like_total += int(item['likes']['count'])
            comment_total += int(item['comments']['count'])
            if item.has_key('video_views'):
                view_total += int(item['video_views'])

    result = {
        'platform': 'instagram',
        'date': today,
        'comment': comment_total,
        'like': like_total,
        'share': 0,
        'dislike': 0,
        'view': view_total
    }
    jsonResult = json.dumps(result)
    print  jsonResult
    return jsonResult

def get_tag_count(tag):
    url = 'https://www.instagram.com/explore/tags/' + str(tag) + '/'
    response = requests.get(url=url, verify=False)
    page = response.text
    pattern = re.compile("window._sharedData = (.+?);</script>", re.S)
    items = re.findall(pattern, page)
    jsonData = json.loads(items[0])
    count = jsonData['entry_data']['TagPage'][0]['tag']['media']['count']
    print count
    return count

if __name__ == "__main__":
    get_by_api()
    # get_tag_count('insta360')