# -*- coding: UTF-8 -*-

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
        self.headers['Authorization'] = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VyIjp7Il9pZCI6IjU3YzdhODA0MmIyZjJkMmZhMWUyMjBmNSIsImZpcnN0TmFtZSI6IkJpYW5jYSIsImxhc3ROYW1lIjoiWmhhbmciLCJlbWFpbCI6ImJpYW5jYUBpbnN0YTM2MC5jb20iLCJwYXNzd29yZCI6IiQyYSQxMCRkQ2tiZnRMbHQzYmROeklxemdqNjMua3daRXdUWnJGMm1XaS5uMVhLTDVERFN0eVg1STNvZSIsImFjdGl2ZUNvbXBhbnlJZCI6IjU3MGRiMjBiZDI1MjQ0NDBiZmVlYzU4MSIsImxhbmd1YWdlIjoiZW4iLCJ0aW1lem9uZSI6IkFzaWEvU2luZ2Fwb3JlIiwiaXNJbnRlcm5hbCI6ZmFsc2UsImNyZWF0ZWQiOiIyMDE2LTA5LTAxVDA0OjAxOjA4LjIyNVoiLCJtb2RpZmllZCI6IjIwMTctMDQtMTdUMDQ6MzI6NDcuNDM3WiIsInRpdGxlIjoiR2xvYmFsIE1hcmtldGluZyBIZWFkIn0sImNvbXBhbnkiOnsiX2lkIjoiNTcwZGIyMGJkMjUyNDQ0MGJmZWVjNTgxIiwibmFtZSI6Ikluc3RhMzYwIC0gRmFpcmhhaXIiLCJjb3VudHJ5IjoiaGsiLCJhY2NvdW50SWQiOjE1Mzg5OTUsIm9wcG9ydHVuaXR5SWQiOjIwOTI0NTEsImNyZWF0ZWQiOiIyMDE2LTA0LTEzVDAyOjQyOjE5LjQ0MloiLCJtb2RpZmllZCI6IjIwMTctMDMtMjlUMDQ6MDQ6MDQuMjEwWiJ9LCJleHAiOjE0OTMxODYxODI1MTh9.NE-vCGKXaLErbTMbJJaj2UP-JNZW9vEds9RfgFu7yEfOHAtkiCpKxV-3fvgP_tiLmx6l2gSQUpnDcynsQZbj5SlYKsXe6hk8G0d1ZGTFMH-SbOIE-1lVA2wEnz-ZlCm_0ECvpDJymiJIUBQtfCIEo6vyriT4FewAFMxogUOZAfm7VM_yOnq8AMVh10vb8MMloJe9rIeEG-iGX_uG_GtuV13KDD_RaMy3FEzPZa5BApo84we413ipIKP1CkM2XyIc6DPfYnmbHzbHETRcodrzCLoF7U_X3OmPHYwrLMPW97pGopMA8avnWF89vrq8dgYK0Jp3u-5fC_WroK--wCqItA'

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
        print json.dumps(result)
        return result


if __name__ == '__main__':
    crawler = MeltwaterCrawler()
    crawler.main('2017-04-01', '2017-04-16')

