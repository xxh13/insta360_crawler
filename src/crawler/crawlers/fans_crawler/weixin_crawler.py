# -*- coding: UTF-8 -*-
'''
官方接口
'''
import urllib2
import json
import urllib


def get_by_api():
    url = 'https://api.weixin.qq.com/cgi-bin/user/get'
    token = get_token()
    value = {}
    value['access_token'] = token
    value['next_openid'] = ''
    data = urllib.urlencode(value)
    request = urllib2.Request(url = url, data = data)
    response = urllib2.urlopen(request)
    page = response.read()
    data = json.loads(page, encoding="utf-8")
    fans = 0
    try:
        fans = data['total']
    except KeyError:
        pass
    print fans
    return fans


def get_token():
    url = 'https://api.weixin.qq.com/cgi-bin/token'
    value = {}
    value['grant_type'] = 'client_credential'
    value['appid'] = 'wxa01ae38d52e5b020'
    value['secret'] = 'ba2229819142d1804cc25edf08c2f045'
    data = urllib.urlencode(value)
    request = urllib2.Request(url = url, data = data)
    response = urllib2.urlopen(request)
    page = response.read()
    print page
    data = json.loads(page, encoding="utf-8")
    result = ''
    try:
        result = data['access_token']
    except KeyError:
        pass
    return result

if __name__ == "__main__":
    get_by_api()