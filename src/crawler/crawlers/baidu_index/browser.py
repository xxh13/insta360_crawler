#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import urllib
import json
import sys
from datetime import datetime, timedelta

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import config
from api import Api
from utils.log import logger
from multi_thread import WorkManager


class BaiduBrowser(object):
    def __init__(self,
                 cookie_json='[{"domain": ".www.baidu.com", "name": "bdime", "expires": "\u5468\u4e00, 20 8\u6708 2046 02:19:54 GMT", "value": "0", "expiry": 2418344394, "path": "/", "httponly": false, "secure": false}, {"domain": ".www.baidu.com", "name": "ORIGIN", "expires": "\u5468\u4e00, 20 8\u6708 2046 02:19:54 GMT", "value": "0", "expiry": 2418344394, "path": "/", "httponly": false, "secure": false}, {"domain": ".www.baidu.com", "name": "sugstore", "expires": "\u5468\u4e00, 20 8\u6708 2046 02:19:54 GMT", "value": "0", "expiry": 2418344394, "path": "/", "httponly": false, "secure": false}, {"domain": ".www.baidu.com", "name": "sug", "expires": "\u5468\u4e00, 20 8\u6708 2046 02:19:54 GMT", "value": "3", "expiry": 2418344394, "path": "/", "httponly": false, "secure": false}, {"domain": "www.baidu.com", "name": "BD_UPN", "expires": "\u5468\u4e8c, 06 9\u6708 2016 02:19:54 GMT", "value": "14314454", "expiry": 1473128394, "path": "/", "httponly": false, "secure": false}, {"domain": ".baidu.com", "name": "BIDUPSID", "expires": "\u5468\u4e09, 19 8\u6708 2048 02:19:54 GMT", "value": "6E1180C96CF46D18311FCEEC15C24788", "expiry": 2481416394, "path": "/", "httponly": false, "secure": false}, {"domain": ".www.baidu.com", "name": "__bsi", "expires": "\u5468\u516d, 27 8\u6708 2016 02:20:00 GMT", "value": "14089856108596563531_00_14_N_N_82_0303_C02F_N_N_N_0", "expiry": 1472264400, "path": "/", "httponly": false, "secure": false}, {"domain": ".baidu.com", "name": "H_PS_PSSID", "value": "1442_18282_17001_11655_20856_20732_20837", "path": "/", "httponly": false, "secure": false}, {"domain": "www.baidu.com", "name": "BD_HOME", "value": "1", "path": "/", "httponly": false, "secure": false}, {"domain": "www.baidu.com", "name": "BD_LAST_QID", "expires": "\u5468\u516d, 27 8\u6708 2016 02:19:55 GMT", "value": "10205523215117148813", "expiry": 1472264395, "path": "/", "httponly": false, "secure": false}, {"domain": ".baidu.com", "name": "PSTM", "expires": "\u5468\u56db, 14 9\u6708 2084 05:34:01 GMT", "value": "1472264394", "expiry": 3619748041, "path": "/", "httponly": false, "secure": false}, {"domain": ".baidu.com", "name": "BDUSS", "expires": "\u5468\u4e09, 13 11\u6708 2024 02:19:52 GMT", "value": "xvLXdJYVQwU252NS03S3JNQXRDTVhXRC1LbmZKcmxtcHB-S1JDYzlFZkloZWhYQVFBQUFBJCQAAAAAAAAAAAEAAABoPjoFa2xxYnRuc25zMTIzAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMj4wFfI-MBXTm", "expiry": 1731464392, "path": "/", "httponly": true, "secure": false}, {"domain": ".baidu.com", "name": "BAIDUID", "expires": "\u5468\u65e5, 27 8\u6708 2017 02:19:48 GMT", "value": "1EAE4A5EF2FD224AAA0D6763DEA3E73B:FG=1", "expiry": 1503800388, "path": "/", "httponly": false, "secure": false}]',
                 # cookie_json='[{"domain": ".i.baidu.com", "name": "Hm_lpvt_4010fd5075fcfe46a16ec4cb65e02f04", "value": "1479133807", "path": "/", "httponly": false, "secure": false}, {"domain": ".i.baidu.com", "name": "Hm_lvt_4010fd5075fcfe46a16ec4cb65e02f04", "expires": "\u5468\u4e8c, 14 11\u6708 2017 14:30:06 GMT", "value": "1479031809,1479131254,1479133718,1479133807", "expiry": 1510669806, "path": "/", "httponly": false, "secure": false}, {"domain": "i.baidu.com", "name": "PHPSESSID", "value": "oggoeleengti7snb2fs2872ln1", "path": "/", "httponly": false, "secure": false}, {"domain": ".baidu.com", "name": "BAIDUID", "expires": "\u5468\u65e5, 27 8\u6708 2017 02:19:48 GMT", "value": "1EAE4A5EF2FD224AAA0D6763DEA3E73B:FG=1", "expiry": 1503771588, "path": "/", "httponly": false, "secure": false}, {"domain": ".baidu.com", "name": "BDUSS", "expires": "\u5468\u4e09, 13 11\u6708 2024 02:19:52 GMT", "value": "xvLXdJYVQwU252NS03S3JNQXRDTVhXRC1LbmZKcmxtcHB-S1JDYzlFZkloZWhYQVFBQUFBJCQAAAAAAAAAAAEAAABoPjoFa2xxYnRuc25zMTIzAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMj4wFfI-MBXTm", "expiry": 1731435592, "path": "/", "httponly": true, "secure": false}, {"domain": ".baidu.com", "name": "PSTM", "expires": "\u5468\u56db, 14 9\u6708 2084 05:34:01 GMT", "value": "1472264394", "expiry": 3619719241, "path": "/", "httponly": false, "secure": false}, {"domain": ".baidu.com", "name": "H_PS_PSSID", "value": "1442_18282_17001_11655_20856_20732_20837", "path": "/", "httponly": false, "secure": false}, {"domain": ".baidu.com", "name": "BIDUPSID", "expires": "\u5468\u4e09, 19 8\u6708 2048 02:19:54 GMT", "value": "6E1180C96CF46D18311FCEEC15C24788", "expiry": 2481387594, "path": "/", "httponly": false, "secure": false}]',
                 check_login=True
                 ):
        if not config.browser_driver:
            browser_driver_name = 'Firefox'
        else:
            browser_driver_name = config.browser_driver
        browser_driver_class = getattr(webdriver, browser_driver_name)
        self.browser = browser_driver_class(service_args=['--ignore-ssl-errors=true','--ssl-protocol=any', '--web-security=true'])
        # 设置超时时间
        self.browser.set_page_load_timeout(50)
        # 设置脚本运行超时时间
        self.browser.set_script_timeout(10)
        # 百度用户名
        self.user_name = config.user_name
        # 百度密码
        self.password = config.password
        self.cookie_json = cookie_json
        self.api = None
        self.cookie_dict_list = []

        self.init_api(check_login=check_login)
        self.get_cookie_json()

    def is_login(self):
        # 如果初始化BaiduBrowser时传递了cookie信息，则检测一下是否登录状态
        self.login_with_cookie(self.cookie_json)
        self.get_cookie_json()

        # 访问待检测的页面
        self.browser.get(config.user_center_url)
        html = self.browser.page_source
        # 检测是否有登录成功标记
        return config.login_sign in html

    def init_api(self, check_login=True):
        # 判断是否需要登录
        need_login = False
        if not self.cookie_json:
            need_login = True
        elif check_login and not self.is_login():
            need_login = True
        # 执行浏览器自动填表登录，登录后获取cookie
        if need_login:
            self.login(self.user_name, self.password)
            self.cookie_json = self.get_cookie_json()
        cookie_str = self.get_cookie_str(self.cookie_json)
        # 获取到cookie后传给api
        self.api = Api(cookie_str)

    def get_date_info(self, start_date, end_date):
        # 如果start_date和end_date中带有“-”，则替换掉
        if start_date.find('-') != -1 and end_date.find('-') != -1:
            start_date = start_date.replace('-', '')
            end_date = end_date.replace('-', '')
        # start_date和end_date转换成datetime对象
        start_date = datetime.strptime(start_date, '%Y%m%d')
        end_date = datetime.strptime(end_date, '%Y%m%d')

        # 循环start_date和end_date的差值，获取区间内所有的日期
        date_list = []
        temp_date = start_date
        while temp_date <= end_date:
            date_list.append(temp_date.strftime("%Y-%m-%d"))
            temp_date += timedelta(days=1)
        start_date = start_date.strftime("%Y-%m-%d")
        end_date = end_date.strftime("%Y-%m-%d")
        return start_date, end_date, date_list

    def get_one_day_index(self, date, url):
        try_num = 0
        try_max_num = 5
        value = ''
        while try_num < try_max_num:
            try:
                try_num += 1
                # 获取图片的下载地址以及图片的切割信息
                img_url, val_info = self.api.get_index_show_html(url)
                # 下载img图片，然后根据css切割图片的信息去切割图片，组成新的图片，
                # 将新图片跟已经做好的图片识别库对应识别
                value = self.api.get_value_from_url(img_url, val_info)
                break
            except:
                pass
        logger.info('date:%s, value:%s' % (date, value))
        return value.replace(',', '')

    def get_baidu_index_by_date_range(self, keyword, start_date, end_date,
                                      type_name):
        # 根据区间获取关键词的索引值
        url = config.time_range_trend_url.format(
            start_date=start_date, end_date=end_date,
            word=urllib.quote(keyword.encode('gbk'))
        )
        self.browser.get(url)
        # 执行js获取后面所需的res和res2的值
        res = self.browser.execute_script('return PPval.ppt;')
        res2 = self.browser.execute_script('return PPval.res2;')

        # 获取指定区间的日期列表,方便下面循环用
        start_date, end_date, date_list = self.get_date_info(
            start_date, end_date
        )

        # 拼接api的url
        url = config.all_index_url.format(
            res=res, res2=res2, start_date=start_date, end_date=end_date
        )
        # 获取api的结果信息，这里面保存了后面日期节点的一些加密值
        all_index_info = self.api.get_all_index_html(url)
        # print all_index_info
        indexes_enc = all_index_info['data'][type_name][0]['userIndexes_enc']
        enc_list = indexes_enc.split(',')

        wm = WorkManager(config.num_of_threads)

        # 遍历这些enc值，这些值拼接出api的url(这个页面返回 图片信息以及css规定的切图信息)
        for index, _ in enumerate(enc_list):
            url = config.index_show_url.format(
                res=res, res2=res2, enc_index=_, t=int(time.time()) * 1000
            )
            # 根据enc在列表中的位置，获取它的日期
            date = date_list[index]
            # 将任务添加到多线程下载模型中
            wm.add_job(date, self.get_one_day_index, date, url)

        wm.start()
        wm.wait_for_complete()

        # 执行结束后，从结果queue中获取到最终的百度指数字典
        baidu_index_dict = wm.get_all_result_dict_from_queue()

        return baidu_index_dict

    def _get_index_period(self, keyword):
        # 拼接一周趋势的url
        url = config.one_week_trend_url.format(
            word=urllib.quote(keyword.encode('gbk'))
        )
        self.browser.get(url)
        # 获取下方api要用到的res和res2的值
        res = self.browser.execute_script('return PPval.ppt;')
        res2 = self.browser.execute_script('return PPval.res2;')
        start_date, end_date = self.browser.execute_script(
            'return BID.getParams.time()[0];'
        ).split('|')
        start_date, end_date, date_list = self.get_date_info(
            start_date, end_date
        )
        url = config.all_index_url.format(
            res=res, res2=res2, start_date=start_date, end_date=end_date
        )
        all_index_info = self.api.get_all_index_html(url)
        start_date, end_date = all_index_info['data']['all'][0][
            'period'].split('|')
        # 重置start_date, end_date，以api返回的为准
        start_date, end_date, date_list = self.get_date_info(
            start_date, end_date
        )
        logger.info('all_start_date:%s, all_end_date:%s' % (start_date, end_date))
        return date_list

    def get_baidu_index(self, keyword, type_name):
        if config.start_date and config.end_date:
            _, _, date_list = self.get_date_info(
                start_date=config.start_date, end_date=config.end_date
            )
        else:
            # 配置文件不配置start_date和end_date，可以查询到这个关键词数据的最大区间
            date_list = self._get_index_period(keyword)

        baidu_index_dict = dict()
        start = 0
        skip = 180
        end = len(date_list)
        while start < end:
            try:
                start_date = date_list[start]
                if start + skip >= end - 1:
                    end_date = date_list[-1]
                else:
                    end_date = date_list[start + skip]
                result = self.get_baidu_index_by_date_range(
                    keyword, start_date, end_date, type_name
                )
                baidu_index_dict.update(result)
                start += skip + 1
            except:
                import traceback

                print traceback.format_exc()
        return baidu_index_dict

    def login(self, user_name, password):
        login_url = config.login_url
        # 访问登陆页
        self.browser.get(login_url)

        # 自动填写表单并提交，如果出现验证码需要手动填写
        user_name_obj = self.browser.find_element_by_id(
            'TANGRAM__PSP_3__userName'
        )
        user_name_obj.send_keys(user_name)
        ps_obj = self.browser.find_element_by_id('TANGRAM__PSP_3__password')
        ps_obj.send_keys(password)
        sub_obj = self.browser.find_element_by_id('TANGRAM__PSP_3__submit')
        # ver_obj = self.browser.find_element_by_id('TANGRAM__PSP_3__verifyCodeImgWrapper')
        # print ver_obj
        try:
            sub_obj.click()
        except WebDriverException, e:
            print e
        # 如果页面的url没有改变，则继续等待
        count = 0
        while self.browser.current_url == login_url:
            time.sleep(1)
            count += 1
            if count >=20:
                sys.exit()

    def close(self):
        self.browser.quit()

    def get_cookie_json(self):
        print json.dumps(self.browser.get_cookies())
        return json.dumps(self.browser.get_cookies())

    def get_cookie_str(self, cookie_json=''):
        if cookie_json:
            cookies = json.loads(cookie_json)
        else:
            cookies = self.browser.get_cookies()
        return '; '.join(['%s=%s' % (item['name'], item['value'])
                          for item in cookies])

    def login_with_cookie(self, cookie_json):
        self.browser.get('https://www.baidu.com/')
        for item in json.loads(cookie_json):
            try:
                self.browser.add_cookie(item)
            except:
                continue
