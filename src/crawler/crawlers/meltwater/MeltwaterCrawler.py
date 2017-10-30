# -*- coding: UTF-8 -*-
from urllib import unquote
import requests
import json
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class MeltwaterCrawler:
    def __init__(self):
        self.country_list = {
            'gb': '英国',
            'de': '德国',
            'jp': '日本',
            'us': '美国',
            'hk': '香港'
        }
        self.url = 'https://ins-services.meltwater.com/volumeService/v2/consolidated'
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
        self.headers = {}
        self.headers['User-Agent'] = user_agent
        self.headers['Host'] = 'ins-services.meltwater.com'
        self.headers['Origin'] = 'https://app.meltwater.com'
        self.headers['Connection'] = 'keep-alive'
        self.headers['Accept'] = 'application/json, text/plain, */*'
        self.headers['Accept-Encoding'] = 'gzip, deflate, br'
        self.headers['Accept-Language'] = 'zh-CN,zh;q=0.8'
        self.headers['Content-Type'] = 'application/json;charset=UTF-8'
        self.headers['Authorization'] = self.login()

        self.params = {}
        # params['dateQueryStart'] = '2017-04-19T06:00:42.263Z'
        self.params['fetchDataForPreviousRange'] = False
        self.params['granularity'] = 'DAY'
        self.params['groupOption'] = 'close'
        self.params['insObject'] = 'dateHistograms'
        self.params['page'] = 0
        self.params['pageSize'] = 999
        self.params['refreshCache'] = True
        self.params['rssFeeds'] = []
        self.params['searchTerm'] = 'real'
        self.params['sortField'] = 'date'
        self.params['sortOrder'] = 'DESC'
        self.params['tags'] = []

    def login(self):
        url = 'https://app.meltwater.com/login'
        headers = {
            'Host': 'app.meltwater.com',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Origin': 'https://app.meltwater.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Referer': 'https://app.meltwater.com/login',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cookie': '_gali=loginForm',
            'Content-Length': '48'
        }
        payload = {
            'username': 'bianca@insta360.com',
            'password': 'Insta360'
        }
        req = requests.post(url, data=payload, headers=headers, verify=False, allow_redirects=False)
        print req.text
        temp = req.cookies['gydaToken']
        temp = unquote(temp)
        temp = json.loads(temp)
        token = temp['token']
        print token
        return token

    def get_social_data(self, start_date, end_date):
        key_dict = {
            '2126793': 'GoPro',
            '2126801': 'Samsung Gear 360',
            '2126797': 'Ricoh Theta',
            '2126795': 'Nokia OZO',
            '1667795': 'Insta360'
        }
        result = []
        self.headers['Referer'] = 'https://app.meltwater.com/dashboard/viewer/5884855031b8e155d9de0558'
        self.params['cacheWidgetId'] = 'widget_1482218859334_1'
        self.params['agents'] = [1667795, 2126795, 2126797, 2126801, 2126793]
        self.params['dateEnd'] = end_date + 'T23:59:59+08:00'
        self.params['dateEndTag'] = end_date + 'T23:59:59+08:00'
        self.params['dateStart'] = start_date + 'T00:00:00+08:00'
        self.params['dateStartTag'] = start_date + 'T00:00:00+08:00'
        for country in self.country_list:
            self.params['country'] = country
            data = json.dumps(self.params)
            req = requests.post(self.url, data=data,headers=self.headers)
            jsonData = json.loads(req.text)
            for item in jsonData['data']:
                for key in item:
                    points = item[key]['datapoints']
                    for point in points:
                        date = point['date'][0:10]
                        value = point['volume']
                        temp = {
                            'key': key_dict[key],
                            'country': self.country_list[country],
                            'date': date,
                            'value': value,
                            'type': 'social'
                        }
                        result.append(temp)
        return result


    def get_news_data(self, start_date, end_date):
        key_dict = {
            '1781649': 'GoPro',
            '1667785': 'Samsung Gear 360',
            '1667779': 'Ricoh Theta',
            '1781659': 'Nokia OZO',
            '1667803': 'Insta360'
        }
        result = []
        self.headers['Referer'] = 'https://app.meltwater.com/dashboard/viewer/5858de8a7759319d12713d45'
        self.params['cacheWidgetId'] = 'widget_1482220401806_6'
        self.params['agents'] = [1781649, 1667779, 1781659, 1667785, 1667803]
        self.params['dateEnd'] = end_date + 'T23:59:59+08:00'
        self.params['dateEndTag'] = end_date + 'T23:59:59+08:00'
        self.params['dateStart'] = start_date + 'T00:00:00+08:00'
        self.params['dateStartTag'] = start_date + 'T00:00:00+08:00'
        for country in self.country_list:
            self.params['country'] = country
            data = json.dumps(self.params)
            req = requests.post(self.url, data=data,headers=self.headers)
            jsonData = json.loads(req.text)
            for item in jsonData['data']:
                for key in item:
                    points = item[key]['datapoints']
                    for point in points:
                        date = point['date'][0:10]
                        value = point['volume']
                        temp = {
                            'key': key_dict[key],
                            'country': self.country_list[country],
                            'date': date,
                            'value': value,
                            'type': 'news'
                        }
                        result.append(temp)
        return result

    def main(self, start_date, end_date):
        result = []
        result.extend(self.get_social_data(start_date, end_date))
        result.extend(self.get_news_data(start_date, end_date))
        return result


if __name__ == '__main__':
    crawler = MeltwaterCrawler()
    crawler.main('2017-09-26', '2017-10-02')

