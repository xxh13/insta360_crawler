# -*- coding: UTF-8 -*-

from django.contrib.auth.models import User
from .config import config

import random
import urllib
import urllib2
import sys
import time

reload(sys)
sys.setdefaultencoding("utf-8")

def password_updater ():
    username = config['username']
    password_list = config['password_list']
    index = random.randint(0, len(password_list) - 1)
    password = password_list[index]
    print password
    user = User.objects.get(username=username)
    user.set_password(password)
    user.save()

    format_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    url = 'http://service.hz.insta360.com/api/dms/sendsinglemail'

    headers = {}
    headers['Authentication-Token'] = config['token']
    str = '<p>bi系统密码于 ' + format_time + ' 自动更新</p>'
    str += '<p>最新账号信息：</p>'
    str += '<p style="margin-left:2em">账号：' + username + '</p>'
    str += '<p style="margin-left:2em">密码：' + password + '</p>'
    value = {}
    value['toAddress'] = config['address_list']
    value['subject'] = '【bi系统】bi系统登录密码更改通知'
    value['htmlBody'] = str
    value['textBody'] = str
    data = urllib.urlencode(value)
    request = urllib2.Request(url=url, data=data, headers=headers)
    response = urllib2.urlopen(request)
    page = response.read()
    print page
    return password