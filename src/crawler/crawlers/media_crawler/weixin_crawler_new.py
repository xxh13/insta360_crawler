# -*- coding: UTF-8 -*-
'''
官方接口
'''
import requests
import json
import urllib
import urllib2
import datetime


def get_by_request():
    url = 'https://api.weixin.qq.com/datacube/getuserread?access_token='
    token = get_token()
    url += token
    now = datetime.datetime.now()
    today = now.strftime('%Y-%m-%d')
    begin_date = (now - datetime.timedelta(days=3)).strftime('%Y-%m-%d')
    end_date = (now - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    data = {
        "begin_date": begin_date,
        "end_date": end_date
    }
    response = requests.post(url = url, data=json.dumps(data), verify=False)
    page = response.text
    data = json.loads(page, encoding="utf-8")
    view = 0
    share = 0
    for item in data['list']:
        view += item['int_page_read_count']
        share += item['share_count']
    result = {
        'platform': 'weixin',
        'date': today,
        'comment': 0,
        'like': 0,
        'share': share,
        'dislike': 0,
        'view': view
    }
    jsonResult = json.dumps(result)
    print  jsonResult
    return jsonResult

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
    get_by_request()