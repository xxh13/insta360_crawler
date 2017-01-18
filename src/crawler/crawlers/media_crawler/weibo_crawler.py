# -*- coding: UTF-8 -*-
'''
官方接口（只能显示最近六条）
最近6条动态的评论、点赞、转发总和
'''
import urllib
import datetime
import time
import json
import requests
import base64


def get_by_api():
    url = 'https://api.weibo.com/2/statuses/user_timeline.json?page=1'
    username = 'newmedia@vzhibo.tv'
    password = 'lanfeng123'
    value = {}
    value['trim_user'] = '1'
    value['count'] = '100'
    value['source'] = '218121934'
    data = urllib.urlencode(value)
    base64string = base64.encodestring(
        '%s:%s' % (username, password))[:-1]  # 注意哦，这里最后会自动添加一个\n
    authheader = "Basic %s" % base64string
    header = {}
    header['Authorization'] = authheader
    now = time.mktime(datetime.date.today().timetuple())
    week_ago = now - (3600 * 24 * 7)
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    share_total = 0
    like_total = 0
    comment_total = 0
    results = requests.get(url=url, params=data, headers=header)
    page = results.content
    jsonData = json.loads(page, encoding="utf-8")
    data = jsonData['statuses']
    for item in data:
        temp = time.mktime(time.strptime(item['created_at'], "%a %b %d %H:%M:%S +0800 %Y"))
        if temp >= week_ago:
            share_total += int(item['reposts_count'])
            like_total += int(item['attitudes_count'])
            comment_total += int(item['comments_count'])
    result = {
        'platform': 'weibo',
        'date': today,
        'comment': comment_total,
        'like': like_total,
        'share': share_total,
        'dislike': 0,
        'view': 0
    }
    jsonResult = json.dumps(result)
    print  jsonResult
    return jsonResult

if __name__ == "__main__":
    get_by_api()