# -*- coding: UTF-8 -*-
'''
官方接口
最近一周动态的点赞、转发总和
'''
import urllib2
import urllib
import json
import time
import datetime
import requests
import ssl
from functools import wraps

def get_by_api():
    username = 'insta360'
    url = 'https://api.twitter.com/1.1/statuses/user_timeline.json?count=200&trim_user=true&contributor_details=false&exclude_replies=true&include_rts=fasle&screen_name=' + username
    oauth = OAuth()
    headers = {}
    headers['Host'] = 'api.twitter.com'
    headers['X-Target-URI'] = 'https://api.twitter.com'
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    headers['Connection'] = 'keep-alive'
    headers['Authorization'] = oauth
    index = 1
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    now = time.mktime(datetime.date.today().timetuple())
    week_ago = now - (3600 * 24 * 7)
    share_total = 0
    like_total = 0
    while(True):
        request = urllib2.Request(url = url + '&page=' + str(index), headers = headers)
        response = urllib2.urlopen(request)
        page = response.read()
        data = json.loads(page, encoding="utf-8")
        for item in data:
            temp = time.mktime(time.strptime(item['created_at'], "%a %b %d %H:%M:%S +0000 %Y"))
            if temp >= week_ago:
                share_total += int(item['retweet_count'])
                like_total += int(item['favorite_count'])
        index += 1
        if len(data) == 0:
            break
    result = {
        'platform': 'twitter',
        'date': today,
        'comment': 0,
        'like': like_total,
        'share': share_total,
        'dislike': 0,
        'view': 0
    }
    jsonResult = json.dumps(result)
    print  jsonResult
    return jsonResult

def get_tag_count(tag):
    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    yesterday = (today - oneday).strftime('%Y-%m-%d')
    base_url = 'https://api.twitter.com/1.1/search/tweets.json'
    url = base_url
    oauth = OAuth()
    headers = {}
    headers['Host'] = 'api.twitter.com'
    headers['X-Target-URI'] = 'https://api.twitter.com'
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    headers['Connection'] = 'keep-alive'
    headers['Authorization'] = oauth
    tag_count = 0
    value = {}
    value['count'] = 200
    value['q'] = '#' + tag + ' ' + 'since:' + yesterday
    value['count'] = 200
    value['count'] = 200
    value = urllib.urlencode(value)
    while (True):
        response = requests.get(url,params = value, headers=headers, verify = False)
        page = response.text
        data = json.loads(page, encoding="utf-8")
        count = len(data['statuses'])
        tag_count += count
        try:
            next = data['search_metadata']['next_results']
            url = base_url + next
        except:
            break
    print tag_count
    return tag_count



def sslwrap(func):
    @wraps(func)
    def bar(*args, **kw):
        kw['ssl_version'] = ssl._PROTOCOL_NAMES
        return func(*args, **kw)
    return bar


def OAuth():
    ssl.wrap_socket = sslwrap(ssl.wrap_socket)
    url = 'https://api.twitter.com/oauth2/token'
    value = {}
    value['grant_type'] = 'client_credentials'
    value['client_id'] = '1VgtHGY9P0MvZCELFMVyj742V'
    value['client_secret'] = 's70lp3naiGFUDhECxCF3oqnvNoDtShIvhEaOqJOZw8Kqkm0Ht4'
    data = urllib.urlencode(value)
    request = urllib2.Request(url = url, data = data)
    response = urllib2.urlopen(request)
    page = response.read()
    data = json.loads(page, encoding="utf-8")
    result = data['token_type'] + ' ' + data['access_token']
    return result

if __name__ == '__main__':
    get_by_api()
    # get_tag_count('insta360')