# -*- coding: UTF-8 -*-
'''
官方接口和第三方接口都可以
'''
import urllib2
import json
import ssl
import urllib
from functools import wraps

#第三方接口
def get_by_request(username='insta360'):
    url = 'https://cdn.syndication.twimg.com/widgets/followbutton/info.json?screen_names=' + username
    request = urllib2.Request(url = url)
    response = urllib2.urlopen(request)
    page = response.read()
    result = json.loads(page, encoding="utf-8")
    fans = result[0]['followers_count']
    print fans
    return fans

#官方接口
def get_by_api():
    username = 'insta360'
    url = 'https://api.twitter.com/1.1/users/show.json?include_entities=fasle&screen_name=' + username
    oauth = OAuth()
    headers = {}
    headers['Host'] = 'api.twitter.com'
    headers['X-Target-URI'] = 'https://api.twitter.com'
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    headers['Connection'] = 'keep-alive'
    headers['Authorization'] = oauth
    request = urllib2.Request(url = url, headers = headers)
    response = urllib2.urlopen(request)
    page = response.read()
    print page
    data = json.loads(page, encoding="utf-8")
    fans = data['followers_count']
    print fans
    return fans


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

def sslwrap(func):
    @wraps(func)
    def bar(*args, **kw):
        kw['ssl_version'] = ssl._PROTOCOL_NAMES
        return func(*args, **kw)
    return bar



if __name__ == "__main__":
    # get_by_api()
    get_by_request()
