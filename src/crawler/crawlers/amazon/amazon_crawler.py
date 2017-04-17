# -*- coding: UTF-8 -*-
'''
使用requests获取网页源文件，通过正则匹配获取评论数
'''
from urls import *   #各国亚马逊网址列表
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
    ssl.wrap_socket = sslwrap(ssl.wrap_socket)  #预防网络请求错误
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


# 获取评论数的思路： 如果页面中出现类似“成为第一个评论该商品的人”的内容，则判断评论数为0， 否则通过正则匹配获取类似“已有n条评论”的内容，拿到评论数。 不同国家,引号中的内容是不一样的，详情见urls.py
def get_comment(url, country):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
        'Upgrade-Insecure-Requests': '1'
    }
    try:
        page = requests.get(url, headers=headers, verify = False, timeout=40)
    except:
        print 'error'
        return 0
    content = page.text.encode('utf-8')
    # 如果页面中出现类似“成为第一个评论该商品的人”的内容，则判断评论数为0
    if first[country] in content:
        print 0
        return 0
    # 否则通过正则匹配获取类似“已有n条评论”的内容，拿到评论数
    try:
        pattern = re.compile('\d+' + review[country], re.S)
        items = re.findall(pattern, content)
        temp = items[0]
        pattern = re.compile('\d+', re.S)
        items = re.findall(pattern, temp)
        sales = (int)(items[0])
        print sales
        return sales
    except:
        print 'error'
        return 0

# stack overflow上抄的
def sslwrap(func):
    @wraps(func)
    def bar(*args, **kw):
        kw['ssl_version'] = ssl.PROTOCOL_TLSv1
        return func(*args, **kw)
    return bar


if __name__ == '__main__':
    main()