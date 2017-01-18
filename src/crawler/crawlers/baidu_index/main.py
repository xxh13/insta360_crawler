#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
使用phantomjs模拟浏览器访问
https://github.com/longzhiwen888/fetch_baidu_index
'''
import traceback
import json

from browser import BaiduBrowser
from utils.log import logger
import config as config


def baidu_index(start_date, end_date):
    logger.info(u'请确保你填写的账号密码能够成功登陆百度')

    s = BaiduBrowser()

    task_list = config.key_list

    type_list = config.index_type_list
    data_list = []
    for keyword in task_list:
        try:
            keyword = keyword.strip()
            if not keyword:
                continue
            keyword_unicode = keyword.decode('utf-8')
            for type_name in type_list:
                baidu_index_dict = s.get_baidu_index_by_date_range(
                    keyword_unicode, start_date, end_date, type_name
                )
                date_list = sorted(baidu_index_dict.keys())

                for date in date_list:
                    value = baidu_index_dict[date]
                    temp = {'key': keyword_unicode, 'date': date, 'baidu_index': value}
                    data_list.append(temp)
        except:
            print traceback.format_exc()
    jsonResult = json.dumps(data_list)
    return jsonResult


if __name__ == "__main__":
    baidu_index('2016-12-12', '2016-12-20')
