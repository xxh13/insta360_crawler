# -*- coding: UTF-8 -*-
'''
官方接口
'''
import urllib2
import json

def get_by_api():
    app_id = '1598022290502419'
    app_secret = 'f0fc5a210b5531987cbc671a6c3d864f'
    access_token = app_id + '|' + app_secret
    username = 'Insta360Camera'
    url = 'https://graph.facebook.com/' + username + '/?fields=fan_count&access_token=' + access_token
    headers = {}
    headers['Host'] = 'graph.facebook.com'
    headers['Connection'] = 'keep-alive'
    headers['Upgrade-Insecure-Requests'] = '1'
    headers['Cache-Control'] = 'max-age=0'

    request = urllib2.Request(url = url, headers = headers)
    response = urllib2.urlopen(request)
    page = response.read()
    # print page
    jsonData = json.loads(page, encoding="utf-8")
    fans = jsonData['fan_count']
    print fans
    return fans

if __name__ == "__main__":
    get_by_api()
