# -*- coding: UTF-8 -*-
'''
官方接口
最近一个月动态的评论、点赞、踩、浏览总和
'''
import urllib2
import urllib
import json
import time
import requests
import datetime
import hashlib

client_id = '138c334850478e6b'
def get_by_api():
    username = 'Insta360'
    url = 'https://openapi.youku.com/v2/videos/by_user.json?client_id=' + client_id + '&user_name=' + username + '&count=20'
    now = time.mktime(datetime.date.today().timetuple())
    week_ago = now - (3600 * 24 * 30)
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    view_total = 0
    like_total = 0
    dislike_total = 0
    comment_total = 0
    request = urllib2.Request(url = url)
    response = urllib2.urlopen(request)
    page = response.read()
    # print page
    jsonData = json.loads(page, encoding="utf-8")
    data = jsonData['videos']
    for item in data:
        temp = time.mktime(time.strptime(item['published'], "%Y-%m-%d %H:%M:%S"))
        if temp >= week_ago:
            view_total += int(item['view_count'])
            dislike_total += int(item['down_count'])
            like_total += int(item['up_count'])
            comment_total += int(item['comment_count'])

    result = {
        'platform': 'youku',
        'date': today,
        'comment': comment_total,
        'like': like_total,
        'share': 0,
        'dislike': dislike_total,
        'view': view_total
    }
    jsonResult = json.dumps(result)
    print  jsonResult
    return jsonResult

def get_tag_count(tag):
    url = 'https://openapi.youku.com/v2/searches/video/by_tag.json?client_id=' + client_id + '&tag=' + tag + '&count=20' + '&period=today'
    request = urllib2.Request(url = url)
    response = urllib2.urlopen(request)
    page = response.read()
    data = json.loads(page, encoding="utf-8")
    # print page
    try:
        count = data['total']
    except:
        count = 0
    print count
    return count

def api_v3():
    url = 'http://openapi.youku.com/router/rest.json?'
    para = {}
    para['q'] = 'videoid:XMjY0NTE3ODAyNA'
    para['fd'] = 'total_vv'
    para['cl'] = 'ns'
    opensysparams = {}
    opensysparams['action'] = 'youku.content.video.single.baseinfo.get'
    opensysparams['client_id'] = client_id
    opensysparams['timestamp'] = str(int(time.time()))
    opensysparams['version'] = '3.0'
    temp = 'action' + urllib.quote(opensysparams['action']) + \
           'cl' + urllib.quote(para['cl']) + \
           'client_id' + urllib.quote(opensysparams['client_id']) + \
           'fd' + urllib.quote(para['fd']) + \
           'q' + urllib.quote(para['q']) +\
           'timestamp' + urllib.quote(opensysparams['timestamp']) +\
           'version' + urllib.quote(opensysparams['version']) + 'secret'
    m = hashlib.md5()
    print urllib.quote(temp)
    m.update(urllib.quote(temp))
    sign = m.hexdigest()
    print sign
    opensysparams['sign'] = sign
    para['opensysparams'] = str(opensysparams)
    for index in para:
        url = url + index + '=' + para[index] + '&'
    print url
    response = requests.get(url)
    print response.text

if __name__ == '__main__':
    # get_by_api()
    # api_v3()
    get_tag_count('insta360')
