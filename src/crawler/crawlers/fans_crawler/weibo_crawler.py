# -*- coding: UTF-8 -*-
'''
urllib2后正则匹配
'''
import re
import urllib2

def get_by_request():
    username = 'insta360'
    url = 'http://weibo.cn/'+ username
    headers = {}
    headers['Host'] = 'weibo.cn'
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0'
    headers['Cookie'] = '_T_WM=d2e28a98d3031cf98e282a29740b5f24'
    request = urllib2.Request(url = url, headers=headers)
    response = urllib2.urlopen(request)
    page = response.read()
    pattern = re.compile("\[(.{0,10})\]</a>&nbsp;<a href=", re.S)
    items = re.findall(pattern, page)
    fans = int(items[1])
    print fans
    return fans


if __name__ == "__main__":
    get_by_request()
