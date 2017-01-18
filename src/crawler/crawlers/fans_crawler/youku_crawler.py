# -*- coding: UTF-8 -*-
'''
官方接口
'''
import urllib2
import json

def get_by_api():
    url = 'https://openapi.youku.com/v2/users/friendship/followers.json?client_id=b10ab8588528b1b1&user_id=UMjk1ODg3NDgwOA=='
    request = urllib2.Request(url = url)
    response = urllib2.urlopen(request)
    page = response.read()
    result = json.loads(page, encoding="utf-8")
    fans = int(result['total'])
    print fans
    return fans

if __name__ == "__main__":
    get_by_api()
