# -*- coding: UTF-8 -*-
'''
官方接口
'''
import urllib2
import json

def get_by_api():
    url = 'https://www.googleapis.com/youtube/v3/channels?part=statistics&id=UC3qWcF49rv8VMZO7Vg6kj5w&key=AIzaSyBg_mtqCgH3mhrTFPVOqDnNeN8wVVO_s5I'
    request = urllib2.Request(url = url)
    response = urllib2.urlopen(request)
    page = response.read()
    result = json.loads(page, encoding="utf-8")
    fans = int(result['items'][0]['statistics']['subscriberCount'])
    print fans
    return fans


if __name__ == "__main__":
    get_by_api()
