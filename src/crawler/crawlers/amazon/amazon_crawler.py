# -*- coding: UTF-8 -*-
from urls import *
import requests
import datetime
import json
import re
import sys
import ssl
from functools import wraps
reload(sys)
sys.setdefaultencoding("utf-8")


def main():
    ssl.wrap_socket = sslwrap(ssl.wrap_socket)
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    result = []
    for i in urls:
        print i
        websites = urls[i]
        total_comment = 0
        for url in websites:
            comment = get_comment(url, i)
            total_comment += comment
        temp = {'commodity': 'insta360 Nano', 'country': i, 'comment': total_comment, 'sale': 0, 'site': 'amazon', 'date': today}
        result.append(temp)
        print temp
    jsonResult = json.dumps(result)
    print jsonResult
    return jsonResult


def get_comment(url, country):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
        'Upgrade-Insecure-Requests': '1'
    }
    try:
        page = requests.get(url, headers=headers)
    except:
        print 'error'
        return 0
    content = page.text.encode('utf-8')
    if first[country] in content:
        print 0
        return 0
    pattern = re.compile('\d+' + review[country], re.S)
    items = re.findall(pattern, content)
    temp = items[0]
    pattern = re.compile('\d+', re.S)
    items = re.findall(pattern, temp)
    sales = (int)(items[0])
    print sales
    return sales


def sslwrap(func):
    @wraps(func)
    def bar(*args, **kw):
        kw['ssl_version'] = ssl.PROTOCOL_TLSv1
        return func(*args, **kw)
    return bar


if __name__ == '__main__':
    main()