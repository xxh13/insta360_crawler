# -*- coding: UTF-8 -*-
'''
使用urllib2，都是通过网页上抓到的接口，主要参数就是start_date和end_date，可以自己定
'''
import datetime
import time
import urllib2
import urllib
import re
import json
import cookielib


class UmengCrawler:
    def __init__(self):
        self.host = 'mobile.umeng.com'
        self.username = 'develop@arashivision.com'
        self.password = '47756ffbee5f356ff8634021622a0d43b3cc046e3d45b319bca8a29593155c08c3c8c49cb0d6029dd8fd8a5c6f8151380a232a701d2277d5289680b373956b1732cb1907afb60c640ac4355eca8d16483b1fbc6eb6eee60df8c6ca9148a1ab91ff9d391626ef088804347c3f27df8e5d8a8f4b265ce596fbe600c2584e17495e'
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'
        self.cookie = 'um_lang=zh; cn_a61627694930aa9c80cf_dplus=%7B%22distinct_id%22%3A%20%2215c2f219e5343a-0e41613148296c-323f5c0f-100200-15c2f219e54b94%22%2C%22sp%22%3A%20%7B%22%24_sessionid%22%3A%200%2C%22%24_sessionTime%22%3A%201495441609%2C%22%24dp%22%3A%200%2C%22%24_sessionPVTime%22%3A%201495441609%7D%2C%22initial_view_time%22%3A%20%221495436487%22%2C%22initial_referrer%22%3A%20%22http%3A%2F%2Fwww.umeng.com%2F%22%2C%22initial_referrer_domain%22%3A%20%22www.umeng.com%22%7D; l=Ap2dqkGOxKFi9LFgehKQBjMPLXOXutEM; aptk_uid=6d72bfdb39f95aa71b4b20dcff67d0b61500979866; umplus_uc_token=1Rar3Af1K0RqClMf3vu-UHw_640ee4f4a6e045e283fc2b5313115d3a; umplus_uc_loginid=develop%40arashivision.com; cn_1259827933_dplus=%7B%22distinct_id%22%3A%20%2215c2f219e5343a-0e41613148296c-323f5c0f-100200-15c2f219e54b94%22%2C%22sp%22%3A%20%7B%22%24_sessionid%22%3A%200%2C%22%24_sessionTime%22%3A%201508491602%2C%22%24dp%22%3A%200%2C%22%24_sessionPVTime%22%3A%201508491602%7D%2C%22initial_view_time%22%3A%20%221508490616%22%2C%22initial_referrer%22%3A%20%22http%3A%2F%2Fpassport.umeng.com%2Fuser%2Fproducts%22%2C%22initial_referrer_domain%22%3A%20%22passport.umeng.com%22%7D; cn_1262440121_dplus=%7B%22distinct_id%22%3A%20%2215c2f219e5343a-0e41613148296c-323f5c0f-100200-15c2f219e54b94%22%2C%22sp%22%3A%20%7B%22%24_sessionid%22%3A%200%2C%22%24_sessionTime%22%3A%201508492690%2C%22%24dp%22%3A%200%2C%22%24_sessionPVTime%22%3A%201508492690%2C%22utm_source%22%3A%20%22banner%22%7D%2C%22initial_view_time%22%3A%20%221508490493%22%2C%22initial_referrer%22%3A%20%22http%3A%2F%2Fwww.umeng.com%2F%22%2C%22initial_referrer_domain%22%3A%20%22www.umeng.com%22%7D; cna=9/yQEVjJDyQCAdOiUVw1VeHL; cn_1258498910_dplus=%7B%22distinct_id%22%3A%20%2215c2f219e5343a-0e41613148296c-323f5c0f-100200-15c2f219e54b94%22%2C%22sp%22%3A%20%7B%22%24recent_outside_referrer%22%3A%20%22%24direct%22%2C%22%24_sessionid%22%3A%200%2C%22%24_sessionTime%22%3A%201508492729%2C%22%24dp%22%3A%200%2C%22%24_sessionPVTime%22%3A%201508492729%7D%2C%22initial_view_time%22%3A%20%221495437365%22%2C%22initial_referrer%22%3A%20%22%24direct%22%2C%22initial_referrer_domain%22%3A%20%22%24direct%22%7D; isg=Ao6OVRb4WxBR-O__f7j_ImqP32Qi26RF3LOgbbjX4hFMGy91IJ_3GKTZJ3CN; umlid_56d95697e0f55a26b5000633=20171020; __utmt=1; cn_1259864772_dplus=%7B%22distinct_id%22%3A%20%2215c2f219e5343a-0e41613148296c-323f5c0f-100200-15c2f219e54b94%22%2C%22USER%22%3A%20%22develop%40arashivision.com%22%2C%22initial_view_time%22%3A%20%221495434670%22%2C%22initial_referrer%22%3A%20%22http%3A%2F%2Fmobile.umeng.com%2Fapps%22%2C%22initial_referrer_domain%22%3A%20%22mobile.umeng.com%22%2C%22%24recent_outside_referrer%22%3A%20%22%24direct%22%2C%22sp%22%3A%20%7B%22%E6%98%AF%E5%90%A6%E7%99%BB%E5%BD%95%22%3A%20false%2C%22%24_sessionid%22%3A%200%2C%22%24_sessionTime%22%3A%201508493297%2C%22%24dp%22%3A%200%2C%22%24_sessionPVTime%22%3A%201508493297%7D%7D; UM_distinctid=15c2f219e5343a-0e41613148296c-323f5c0f-100200-15c2f219e54b94; CNZZDATA1259864772=89266695-1508490106-http%253A%252F%252Fpassport.umeng.com%252F%7C1508490106; ummo_ss=BAh7CUkiGXdhcmRlbi51c2VyLnVzZXIua2V5BjoGRVRbCEkiCVVzZXIGOwBGWwZvOhNCU09OOjpPYmplY3RJZAY6CkBkYXRhWxFpW2kB2WlbaQGXaQHgaQH1aV9pK2kBtWkAaQtpOEkiGUp2SFpFRmMwaXlMUlQ2MmJDQ3lCBjsAVEkiFHVtcGx1c191Y190b2tlbgY7AEYiPTFSYXIzQWYxSzBScUNsTWYzdnUtVUh3XzY0MGVlNGY0YTZlMDQ1ZTI4M2ZjMmI1MzEzMTE1ZDNhSSIQX2NzcmZfdG9rZW4GOwBGSSIxdUFSeU5TTkJkYm81b2NpaXY3SUF4YnI5WEd3Z0JZRytxV3FwRkcxak9GUT0GOwBGSSIPc2Vzc2lvbl9pZAY7AFRJIiUwMmY3MTVhMmIzMWNmOWFkYjQxYWM4YTlkMjAxYjQ5NAY7AEY%3D--ca84417eba89cdfa11dbb29e9e7d1624c7c68466; __utma=151771813.6576068.1508492732.1508492732.1508492732.1; __utmb=151771813.8.9.1508492750086; __utmc=151771813; __utmz=151771813.1508492732.1.1.utmcsr=passport.umeng.com|utmccn=(referral)|utmcmd=referral|utmcct=/user/products;'
        self.headers = {}
        self.headers['User-Agent'] = self.user_agent
        self.headers['Host'] = self.host
        self.headers['X-Requested-With'] = 'XMLHttpRequest'
        self.headers['Connection'] = 'keep-alive'
        self.headers['Cache-Control'] = 'max-age=0'
        self.headers['Accept'] = '*/*'
        self.headers['Accept-Language'] = 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'
        self.headers['X-CSRF-Token'] = 'uARyNSNBdbo5ociiv7IAxbr9XGwgBYG+qWqpFG1jOFQ=/gFNp1sCqJZA='
        self.apps = {
            'nano': 'cf41008f4de85e761c647675',
            'air': 'ebb10037566d6b56c766c985'
    }
        self.start()

    #使用urllib2 登录，获取登陆后的cookie并保存
    def start(self):
        request = urllib2.Request('https://i.umeng.com')
        response = urllib2.urlopen(request)
        page = response.read()
        pattern = re.compile("token: '.*'", re.S)
        items = re.findall(pattern, page)
        token = items[0][8:40]
        pattern = re.compile("sessionid: '.*'", re.S)
        items = re.findall(pattern, page)
        sessionid = items[0][12:52]
        date = str(int(time.time()))
        cookie = cookielib.CookieJar()
        handler = urllib2.HTTPCookieProcessor(cookie)
        opener = urllib2.build_opener(handler)

        values = {
            'loginId': self.username,
            'password2': self.password,
            'checkCode': '',
            'appName': 'youmeng',
            'appEntrance': 'default',
            'bizParams': '',
            'ua': '099#KAFEc7E9EG5E6YTLEEEEE6twSXv7V6D1DXRqD6VqZRso+fPTguBIn6VcZXC6+fYBYRXjAIdBYc37DIgFDcZj+MtTYRwYgybTET/sudyl0yaSt3xRO9uRSf8D8lCgPow3YXc0dqSLE7EjllsllVRC4/l0Py80g6R0bKEnE7EKt37Bldcdt3bi4GFEJcBNlllPbaTk8yxPrMOm8OXFVovK8PchQUiNCo49E7EFD67EEwoTETillAlldsaSurhJby1TSV3W8OXgLybTET9llC3ldRaSt3ilG/uRSf8D8lCgPowm41qTETJll/llV/Wxlt8Dr08FSP8G4RbTET9llC3ldRaSt3ilL3uRSf8D8lCgPowm4K5TEEiStEE7JGFET6i5EE1lE7EFNIaHF7oTEEySl3llsyCzE7TxT1ywEF2So87YqIWoyeHSoZdYkfMl+wDzkLp6mCXGkLKo3jk36OT26HGbvFdWVwICRJ9yk8lDqwP+M6A0pu7WoZjDB0ANtkj26HA3nkps0kVZkUoTEja5R713aquYSpXfNV9c1e95zqbVcLSpr6hZDahG3MesD/rkPwoq+yLBbtUnHda3rM2QZiXaEm1dQs90FswcazOsrfCX/IS3rfCWnjcGabWjlWwxbwXp1u86bfXGrbn3dUhYZi2CAA14GX8IrLe6csy9O/WGc7U6zVOCvRoWAMZDSM9SPCbq1WcXU6pWbLP6rdu9uOIQAMZaZOeJqsw6LOhB/oW8PSUqr6nzLsEZLY/C4295KOj6Lc8TU67Qr5TtuQrDAO4QL5WYLeJqbLXR3y9Mr02ArMVtr6XaZLX4xSWDZRh9by8ccWyIbISMHlWusflLDzry3/lvSXwk8Azlapw5zKWBNdQpztx4Ca4W37uVnROfHsh6w9rBrtCS6WSTE1LSt3llsyaSt3iSE6iP/37mt377mXZdtl9StTTmsyaZR/iSFHBP/3MrJ7FE13iSEJv5+WmkOGFET/yZTEwyL25TEEi5D7EE6GFE19iS0llR/3iurioTETilla3ldOaSl871by1TSV3W8OXgLioTETillC3ldRaSlgTZby1TSV3W8OXgLjdTEEi5DEEEJGFET6i5EE1iE7ExllllluZa5w20PpZV+Pk2PVnVIGFEHuB4lll+XKRlZykV8MixZ28mVbv0YbW7JGFET6i5EEELE7EBVXBlluKX4/l0Py80g6R0e0B8Cf81azELE7EjllllllAh4/l0Py80g6R0bKE9E7EFD67EE1qTETJlllll4L+xlt8Dr08FSP8G4E==',
            'hsid': '1e9bc7bacdcf45193faa7c688b1ca2e4',
            'rdsToken': '',
            'umidToken': '9f7b57fb270885cb6aa7d1aaac45f259dba7a08a',
            'isRequiresHasTimeout': 'false',
            'isRDSReady': 'true',
            'isUMIDReady': 'isUMIDReady',
            'umidGetStatusVal': '255',
            'lrfcf': '',
            'lang': 'zh_cn',
            'scene': '',
            'isMobile': 'false',
            'screenPixel': '1366x768',
            'navlanguage': 'zh-CN',
            'navUserAgent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'navAppVersion': '',
            'navPlatform': '',
            'token': '',
            'nocAppKey': '',
            'csessionid': '',
            'sig': '',
            'captchaToken': '',
            '_csrf_token': '94mc6VOhSa3QP56XjC6IK2'
        }
        headers = {}
        headers['X-Requested-With'] = 'XMLHttpRequest'
        headers['User-Agent'] = self.user_agent
        headers['Host'] = 'passport.alibaba.com'
        headers['Origin'] = 'https://passport.alibaba.com'
        headers['X-Requested-With'] = 'XMLHttpRequest'
        headers['Connection'] = 'keep-alive'
        headers['Referer'] = 'https://passport.alibaba.com/mini_login.htm?lang=zh_cn&appName=youmeng&appEntrance=default&styleType=auto&bizParams=&notLoadSsoView=true&notKeepLogin=false&isMobile=false&cssLink=https://passport.umeng.com/css/loginIframe.css&rnd=0.10927577253646747'
        headers['Accept'] = '*/*'
        headers['Accept-Language'] = 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'
        headers[
            'Cookie'] = 't=8c2104b33f867314978f96da2f8a0ebf; _uab_collina=149579075934407755601457; l=Ao2N3XY1fYyFMIEwisLgeAJFHaMHZcE8; umdata_=70CF403AFFD707DF176342C07955D504071D3D712F4B45002F4EEB3197D2A03B38176EB3779BD52FCD43AD3E795C914C8C2179C0ABC2185A05246EC8E1B8CA84; v=0; cookie2=1e9bc7bacdcf45193faa7c688b1ca2e4; _tb_token_=e5a655781be1b; cna=9/yQEVjJDyQCAdOiUVw1VeHL; _umdata=BA335E4DD2FD504FDB20DB1838C74A33177126C1B6E55BEEC360D0D04DFD01DA81AB19C07EE20598CD43AD3E795C914CF0C3A6A1F8AEEFE87C3135A0A02F5B22; isg=At_f4Zou-n_1YP5j2EQ7wzBgbjMbkMWq9fiRWnEsSw7VAPyCexRxNtWWtqeE'
        data = urllib.urlencode(values)
        request = urllib2.Request(url='https://passport.alibaba.com/newlogin/login.do?fromSite=-2&appName=youmeng', data=data, headers=headers)
        result = opener.open(request)
        print result.read()
        for c in cookie:
            self.cookie += c.name + '=' + c.value + ';'
        self.headers['Cookie'] = self.cookie

    # 获取新增用户
    def getNewUser(self, start_date, end_date, appid):
        self.headers['Referer'] = 'http://mobile.umeng.com/apps/' + appid + '/reports/installation'
        request = urllib2.Request(
            'http://mobile.umeng.com/apps/' + appid + '/reports/load_table_data?page=1&per_page=99999&start_date=' + start_date + '&end_date=' + end_date + '&versions[]=&channels[]=&segments[]=&time_unit=daily&stats=installations',
            headers=self.headers)
        try:
            response = urllib2.urlopen(request)
            jsonData = response.read()
            result = json.loads(jsonData, encoding="utf-8")
            return result['stats']
        except urllib2.URLError, e:
            if hasattr(e, "code"):
                print e.code
            if hasattr(e, "reason"):
                print e.reason

    #获取活跃用户
    def getActiveUser(self, start_date, end_date, appid):
        self.headers['Referer'] = 'http://mobile.umeng.com/apps/' + appid + '/reports/active_user'
        request = urllib2.Request(
            'http://mobile.umeng.com/apps/' + appid + '/reports/load_table_data?page=1&per_page=99999&start_date=' + start_date + '&end_date=' + end_date + '&versions[]=&channels[]=&segments[]=&time_unit=daily&stats=active_users',
            headers=self.headers)
        try:
            response = urllib2.urlopen(request)
            jsonData = response.read()
            result = json.loads(jsonData, encoding="utf-8")
            # print result['stats']
            return result['stats']
        except urllib2.URLError, e:
            if hasattr(e, "code"):
                print e.code
            if hasattr(e, "reason"):
                print e.reason

    # 获取使用时长
    def getDuration(self, date, appid):
        self.headers['Referer'] = 'http://mobile.umeng.com/apps/' + appid + '/reports/duration'
        request = urllib2.Request(
            'http://mobile.umeng.com/apps/' + appid + '/reports/load_chart_data?start_date=' + date + '&end_date=' + date + '&versions[]=&channels[]=&segments[]=&time_unit=daily&stats=duration&stat_type=daily',
            headers=self.headers)
        try:
            response = urllib2.urlopen(request)
            jsonData = response.read()
            result = json.loads(jsonData, encoding="utf-8")
            return result['summary']['value']
        except urllib2.URLError, e:
            if hasattr(e, "code"):
                print e.code
            if hasattr(e, "reason"):
                print e.reason

    #使用情况
    def getUseCondition(self, start_date, end_date):
        result = []
        for app in self.apps:
            appid = self.apps[app]
            newUser = self.getNewUser(start_date, end_date, appid)
            activeUser = self.getActiveUser(start_date, end_date, appid)
            start = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
            end = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
            for i in range((end - start).days + 1):
                date = (end - datetime.timedelta(days=i)).strftime('%Y-%m-%d')
                durationStr = self.getDuration(date, appid)
                temp = durationStr.split(':')
                duration = int(temp[0]) * 3600 + int(temp[1]) * 60 + int(temp[2])
                temp = {'date': date, 'new_user': newUser[i]['data'], 'active_user': activeUser[i]['data'],
                        'duration': duration, 'product': app}
                result.append(temp)
        jsonResult = json.dumps(result)
        return jsonResult


    def getTotalError(self, start_date, end_date):
        result = []
        for app in self.apps:
            appid = self.apps[app]
            self.headers['Referer'] = 'http://mobile.umeng.com/apps/' + appid + '/error_types/trend'
            request = urllib2.Request(
                'http://mobile.umeng.com/apps/' + appid + '/reports/load_chart_data?start_date=' + start_date + '&end_date=' + end_date + '&stats=error_count',
                headers=self.headers)
            try:
                response = urllib2.urlopen(request)
                jsonData = response.read()
                res = json.loads(jsonData, encoding="utf-8")
                data = res['stats'][0]['data']
                dates = res['dates']
                for index in range(len(dates)):
                    temp = {'date': dates[index], 'total_error': data[index], 'product': app}
                    result.append(temp)
            except urllib2.URLError, e:
                if hasattr(e, "code"):
                    print e.code
                if hasattr(e, "reason"):
                    print e.reason
        jsonResult = json.dumps(result)
        return jsonResult

    # 错误率
    def getErrorRate(self, start_date, end_date):
        result = []
        for app in self.apps:
            appid = self.apps[app]
            self.headers['Referer'] = 'http://mobile.umeng.com/apps/' + appid + '/reports/trend_summary'
            request = urllib2.Request(
                'http://mobile.umeng.com/apps/' + appid + '/reports/load_chart_data?start_date=' + start_date + '&end_date=' + end_date + '&stats=trend_error_rate',
                headers=self.headers)
            try:
                response = urllib2.urlopen(request)
                jsonData = response.read()
                res = json.loads(jsonData, encoding="utf-8")
                data = res['stats'][0]['data']
                dates = res['dates']
                for index in range(len(dates)):
                    temp = {'date': dates[index], 'error_rate': data[index], 'product': app}
                    result.append(temp)
            except urllib2.URLError, e:
                if hasattr(e, "code"):
                    print e.code
                if hasattr(e, "reason"):
                    print e.reason
        jsonResult = json.dumps(result)
        return jsonResult

    #错误情况（未用到）
    def getErrorDetail(self, start_date, end_date):
        # start_date 必须在今天的前15天之后
        self.headers['Referer'] = 'http://mobile.umeng.com/apps/cf41008f4de85e761c647675/error_types'
        request = urllib2.Request(
            'http://mobile.umeng.com/apps/cf41008f4de85e761c647675/error_types/search?start_date=' + start_date + '&end_date=' + end_date + '&versions[]=1.2.0&versions[]=1.2.1&versions[]=1.1.0&message_type=legit&per_page=99999&page=0&order_by=desc_error_count',
            headers=self.headers)
        try:
            response = urllib2.urlopen(request)
            jsonData = response.read()
            result = json.loads(jsonData, encoding="utf-8")
            return result['result']
        except urllib2.URLError, e:
            if hasattr(e, "code"):
                print e.code
            if hasattr(e, "reason"):
                print e.reason


    def getUserCityDistribution(self, start_date, end_date , appid):
        self.headers['Referer'] = 'http://mobile.umeng.com/apps/' + appid + '/reports/location?which=cities'
        request = urllib2.Request(
            'http://mobile.umeng.com/apps/' + appid + '/reports/load_table_data?page=1&per_page=99999&start_date=' + start_date + '&end_date=' + end_date + '&versions[]=&channels[]=&segments[]=&time_unit=daily&stats=location_cities',
            headers=self.headers)
        try:
            response = urllib2.urlopen(request)
            jsonData = response.read()
            result = json.loads(jsonData, encoding="utf-8")
            return result['stats']
        except urllib2.URLError, e:
            if hasattr(e, "code"):
                print e.code
            if hasattr(e, "reason"):
                print e.reason
        except KeyError:
            return {}


    def getUserCountryDistribution(self, start_date, end_date, appid):
        self.headers[
            'Referer'] = 'http://mobile.umeng.com/apps/' + appid + '/reports/location?which=countries'
        request = urllib2.Request(
            'http://mobile.umeng.com/apps/' + appid + '/reports/load_table_data?page=1&per_page=99999&start_date=' + start_date + '&end_date=' + end_date + '&versions[]=&channels[]=&segments[]=&time_unit=daily&stats=location_countries',
            headers=self.headers)
        try:
            response = urllib2.urlopen(request)
            jsonData = response.read()
            result = json.loads(jsonData, encoding="utf-8")
            return result['stats']
        except urllib2.URLError, e:
            if hasattr(e, "code"):
                print e.code
            if hasattr(e, "reason"):
                print e.reason
        except KeyError:
            return {}

    #用户分布
    def getUserDistribution(self, start_date, end_date):
        start = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        end = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
        result = []
        for app in self.apps:
            appid = self.apps[app]
            for i in range((end - start).days + 1):
                date = (end - datetime.timedelta(days=i)).strftime('%Y-%m-%d')
                city = self.getUserCityDistribution(date, date, appid)
                for item in city:
                    is_native = 1
                    if item['date'] == '香港' or item['date'] == '台湾' or item['date'] == '澳门':
                        is_native = 0
                    try:
                        active_rate = float(item['active_rate'])
                    except:
                        active_rate = 0
                    try:
                        launch_rate = float(item['launch_rate'])
                    except:
                        launch_rate = 0
                    try:
                        new_rate = float(item['install_rate'])
                    except:
                        new_rate = 0
                    temp = {'date': date, 'location': item['date'], 'active_user': item['active_data'],
                            'active_rate': active_rate, 'new_user': item['install_data'],
                            'new_rate': new_rate, 'launch_data': launch_rate,
                            'launch_rate': item['launch_rate'], 'is_native': is_native, 'product': app}
                    result.append(temp)
                country = self.getUserCountryDistribution(date, date, appid)
                for item in country:
                    temp = {'date': date, 'location': item['date'], 'active_user': item['active_data'],
                            'active_rate': item['active_rate'], 'new_user': item['install_data'],
                            'new_rate': item['install_rate'], 'launch_data': item['launch_data'],
                            'launch_rate': item['launch_rate'], 'is_native': 0, 'product': app}
                    result.append(temp)
        jsonResult = json.dumps(result)
        return jsonResult

    #获取自定义事件
    def getEvent(self, start_date, end_date, event_group_id, version, appid):
        self.headers['Referer'] = 'http://mobile.umeng.com/apps/' + appid + '/events/' + event_group_id + '?version='
        request = urllib2.Request(
            'http://mobile.umeng.com/apps/' + appid + '/events/load_table_data?page=1&per_page=99999&start_date=' + start_date + '&end_date=' + end_date + '&versions[]=' + version + '&channels[]=&stats=event_group_trend&event_group_id=' + event_group_id,
            headers=self.headers
        )
        try:
            response = urllib2.urlopen(request)
            jsonData = response.read()
            result = json.loads(jsonData, encoding="utf-8")
            return result['stats']
        except urllib2.URLError, e:
            if hasattr(e, "code"):
                print e.code
            if hasattr(e, "reason"):
                print e.reason

    #获取版本号
    def getVersions(self, appid):
        self.headers['Referer'] = 'http://mobile.umeng.com/apps/' + appid + '/events/dashboard'
        request = urllib2.Request(
            'http://mobile.umeng.com/apps/' + appid + '/load_versions?show_all=true',
            headers=self.headers
        )
        try:
            response = urllib2.urlopen(request)
            jsonData = response.read()
            print jsonData
            result = json.loads(jsonData, encoding="utf-8")
            datas = result['datas']
            versions = []
            for data in datas:
                versions.append(data['name'])
            return versions
        except urllib2.URLError, e:
            if hasattr(e, "code"):
                print e.code
            if hasattr(e, "reason"):
                print e.reason

    #分享渠道
    def getShareChannel(self, start_date, end_date):
        event_group_ids = {
            'nano': {
                '微信_img': '57afe74767e58ea4ca000428',
                'Facebook_img': '57afe75ce0f55a34db00349c',
                'Whatsapp_img': '57afe7a267e58edf73002e91',
                'Facebook_video': '57afe6ce67e58eb85a0046e5',
                '链接_video': '5858e1fdf5ade402780010ac',
                '微信_video': '57afe6bee0f55a480400445a',
                'Line_img': '57afe7bce0f55ac27900447b',
                'Whatsapp_video': '57afe71b67e58e317b003814',
                'Moment_img': '57afe78567e58e3c1f001b74',
                'Instagram_video': '5858e1f17666135f19000550',
                '链接_img': '5858e214f5ade44ac9000fce',
                'Youtube_video': '57afe6ed67e58e84230001c1',
                'Messenger_img': '57afe7af67e58e7837001ac7',
                'Line_video': '57afe73767e58e6bc80006b2',
                'Instagram_img': '5858e209c895765ac5001b99',
                '朋友圈_video': '57afe70067e58e86c5003cfe',
                'Messenger_video': '57afe728e0f55a7b52002ba4',
                'QQ_img': '57afed8667e58e42aa0005da',
                '微博_video': '57afe70e67e58e5f2f005a1e',
                'QQ_video': '57afed9f67e58eb85a004bfd',
                'Twitter_img': '57afe76b67e58ef70b003503',
                '微博_img': '57afe794e0f55ac8e3000e81',
                'Qzone_video': '57afedaa67e58e6bc8000c4d',
                'Twitter_video': '57afe6dd67e58e86ad000af7',
                'Qzone_img': '57afed9267e58e4759002409'
            },
            'air': {
            }
        }
        min_version = {
            'nano': '1.3.0',
            'air': '1.0.0'
        }
        result = []
        for app in self.apps:
            appid = self.apps[app]
            versions = self.getVersions(appid)
            for version in versions:
                if self.compareVersion(version, min_version[app]) < 0:
                    continue
                for index in event_group_ids[app]:
                    event_group_id = event_group_ids[app][index]
                    data = self.getEvent(start_date, end_date, event_group_id, version, appid)
                    temps = index.split('_')
                    temp = {
                        'version': version,
                        'event_group_id': event_group_id,
                        'channel': temps[0],
                        'type': temps[1],
                        'data': data,
                        'product': app
                    }
                    result.append(temp)
        jsonResult = json.dumps(result)
        return jsonResult

    #分享模式
    def getShareMode(self, start_date, end_date):
        event_group_ids = {
            'nano': {
                '截图': '58817174bbea834daf0000f5',
                '全景图片': '58817174bbea834daf0000f4',
                '全景视频': '58817174bbea834daf0000f7',
                '动画': '58817174bbea834daf0000f6',
            },
            'air': {
                '截图': '589c669176661359a0000f9d',
                '全景图片': '589c669176661359a0000f9c',
                '全景视频': '589c669176661359a0000f9f',
                '动画': '589c669176661359a0000f9e',
            }
        }
        min_version = {
            'nano': '1.7.0',
            'air': '1.0.0'
        }
        result = []
        for app in self.apps:
            appid = self.apps[app]
            versions = self.getVersions(appid)
            for version in versions:
                if self.compareVersion(version, min_version[app]) < 0:
                    continue
                for index in event_group_ids[app]:
                    event_group_id = event_group_ids[app][index]
                    data = self.getEvent(start_date, end_date, event_group_id, version, appid)
                    temp = {
                        'version': version,
                        'event_group_id': event_group_id,
                        'mode': index,
                        'data': data,
                        'product': app
                    }
                    result.append(temp)
        jsonResult = json.dumps(result)
        return jsonResult

    #分享转化率
    def getShareCount(self, start_date, end_date):
        event_group_ids = {
            'nano': {
                'video_success': '576ba13767e58eb24f001ee5',
                'video_try': '576ca33267e58e9c380026a4',
                'img_try': '576ca36067e58ed3450030a8',
                'img_success': '576ba15a67e58e15b2001435'
            },
            'air': {
            }
        }
        min_version = {
            'nano': '1.6.0',
            'air': '1.0.0'
        }
        result = []
        for app in self.apps:
            appid = self.apps[app]
            versions = self.getVersions(appid)
            for version in versions:
                if self.compareVersion(version, min_version[app]) < 0:
                    continue
                for index in event_group_ids[app]:
                    event_group_id = event_group_ids[app][index]
                    data = self.getEvent(start_date, end_date, event_group_id, version, appid)
                    temps = index.split('_')
                    temp = {
                        'version': version,
                        'event_group_id': event_group_id,
                        'data': data,
                        'type': temps[0],
                        'flag': temps[1],
                        'product': app
                    }
                    result.append(temp)
        jsonResult = json.dumps(result)
        return jsonResult

    #拍照、摄像数
    def getTakeCount(self, start_date, end_date):
        event_group_ids = {
            'nano': {
                'video': '5767490667e58e557e002902',
                'img': '5767490667e58e557e00290a'
            },
            'air': {
                'video': '589c669176661359a0000f60',
                'img': '589c669176661359a0000f5e'
            }
        }
        min_version = {
            'nano': '1.2.0',
            'air': '1.0.0'
        }
        result = []
        for app in self.apps:
            appid = self.apps[app]
            versions = self.getVersions(appid)
            versions.append('')
            for version in versions:
                if self.compareVersion(version, min_version[app]) < 0 and version != '':
                    continue
                for index in event_group_ids[app]:
                    event_group_id = event_group_ids[app][index]
                    data = self.getEvent(start_date, end_date, event_group_id, version, appid)
                    v = version
                    if v == '':
                        v = 'all'
                    temp = {
                        'version': v,
                        'event_group_id': event_group_id,
                        'data': data,
                        'type': index,
                        'product': app
                    }
                    result.append(temp)
        jsonResult = json.dumps(result)
        return jsonResult

    def compareVersion(self, version1, version2):
        temp1 = version1.split('.')
        temp2 = version2.split('.')
        ver1 = [0, 0, 0]
        ver2 = [0, 0, 0]
        for index in range(len(ver1)):
            try:
                num = int(temp1[index])
            except:
                num = 0
            ver1[index] += num

        for index in range(len(ver2)):
            try:
                num = int(temp2[index])
            except:
                num = 0
            ver2[index] += num

        for index in range(len(ver1)):
            if (ver1[index] < ver2[index]):
                return -1
            if (ver1[index] > ver2[index]):
                return 1
            continue
        return 0


if __name__ == "__main__":
    crawler = UmengCrawler()
    print crawler.getTakeCount('2017-09-25', '2017-09-27')