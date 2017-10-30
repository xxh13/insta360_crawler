# -*- coding: UTF-8 -*-
'''
官方接口
最近一周动态的评论、点赞、转发总和
'''
import urllib2
import json
import time
import datetime
import requests

app_id = '143580116255494'
app_secret = '62772cd2ae4727853b36d722fcb9e43d'
# app_id = '1586202924770913'
# app_secret = '2232dc879a06f476e6b8af45d256a3c7'
# app_id = '163680667532581'
# app_secret = '7f5cedfb05643f115af57a6f120fd213'
# app_id = '1598022290502419'
# app_secret = 'f0fc5a210b5531987cbc671a6c3d864f'
access_token = app_id + '|' + app_secret

def get_by_api():
    username = 'Insta360Official'
    url = 'https://graph.facebook.com/' + username + '/posts?fields=shares,message,comments.limit(0).summary(true),likes.limit(0).summary(true),created_time,id,link&limit=100&access_token=' + access_token
    headers = {}
    headers['Host'] = 'graph.facebook.com'
    headers['Connection'] = 'keep-alive'
    headers['Upgrade-Insecure-Requests'] = '1'
    headers['Cache-Control'] = 'max-age=0'
    now = time.mktime(datetime.date.today().timetuple())
    week_ago = now - (3600 * 24 * 7)
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    share_total = 0
    like_total = 0
    comment_total = 0
    while True:
        time.sleep(3)
        # request = urllib2.Request(url = url, headers = headers)
        # response = urllib2.urlopen(request)
        # page = response.read()
        response = requests.get(url=url, headers=headers, verify=False)
        page = response.text
        jsonData = json.loads(page, encoding="utf-8")
        data = jsonData['data']
        for item in data:
            share = item['shares']['count'] if item.has_key('shares') else 0
            temp = time.mktime(time.strptime(item['created_time'], "%Y-%m-%dT%H:%M:%S+0000"))
            if temp >= week_ago:
                share_total += int(share)
                like_total += int(item['likes']['summary']['total_count'])
                comment_total += int(item['comments']['summary']['total_count'])
        if len(data) == 0:
            break
        paging = jsonData['paging'] if jsonData.has_key('paging') else {}
        url = paging['next'] if paging.has_key('next') else ''
        if url == '':
            break
    result = {
        'platform': 'facebook',
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


if __name__ == '__main__':
    get_by_api()