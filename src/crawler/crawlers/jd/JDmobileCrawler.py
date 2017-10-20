# -*- coding: UTF-8 -*-


from Commodity_new import Commodity

import datetime
import requests
import socket
import json
import sys


reload(sys)
sys.setdefaultencoding("utf-8")
timeout = 99999999
socket.setdefaulttimeout(timeout)


class JDCrawler:
    def __init__(self):
        self.commodityList = []
        self.url = 'https://so.m.jd.com/ware/searchList.action'
        # user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
        # self.headers = {
        #     'user-agent': user_agent,
        #     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        #     'referer': 'https://so.m.jd.com/ware/search.action',
        #     'upgrade-insecure-requests': '1',
        #     'cookie': 'JAMCookie=true; user-key=dfcf8bf4-aefa-4bac-8b72-f151b02c979e; cn=0; unpl=V2_ZzNtbUtWRUEhWkNVfU0OAGIFF1USB0MScF9FVXkfDFdnAEJcclRCFXMUR1FnGVwUZwYZXEVcRhdFCHZXfBpaAmEBFl5yBBNNIEwEACtaDlwJABNdQF9DFnQMQmRLGlw1ZwIiXUdfQxJ3CkJRchFdBWULEltEUkccdzh2U0spbAVvChVbSmdCJXQ4BAAnEF8BZgoaEEJSSxVyCkRQfhBUBGcBGl1EUUYRfAp2VUsa; abtest=20170411141011523_77; __jdv=122270672|androidapp|t_335139774|appshare|CopyURL|1491891438049; warehistory="11006823274,"; ipLoc-djd=1-72-2799-0; ipLocation=%u5317%u4EAC; 3AB9D23F7A4B3C9B=Q53U4PSU7JUCXUT4UALE2L3NQKT3IWCMU44ZUMB3JXHYHJM3T7HG7DQ5EYLIRYE4WOC3DV2OW6VV3OZIIYNIT6DKFI; mobilev=html5; USER_FLAG_CHECK=0205f1df387d9d65321e9f62fed5df6a; sid=b700be1ab90e5998119ec588e120f3a4; __jda=122270672.1491633548901391774583.1491633549.1492058140.1492065791.8; __jdb=122270672.4.1491633548901391774583|8.1492065791; __jdc=122270672; mba_muid=1491633548901391774583; __jdu=1491633548901391774583; mba_sid=14920657912313869010150644889.4; M_Identification=4d9cf58990296ef5_11ad152bb0360824e98ddd9e1d4e5e00; M_Identification_abtest=20170411141804142_74628842; JSESSIONID=50C066F0FA72DCCF13152EE1FFF2A125.s1; __utmmobile=0x7115902fa6750c1e; M_Identification=4d9cf58990296ef5_11ad152bb0360824e98ddd9e1d4e5e00',
        #     'cache-control': 'max-age=0',
        #     'accept-language': 'zh-CN,zh;q=0.8',
        #     'accept-encoding': 'gzip, deflate, sdch, br'
        # }
        self.products ={
            'insta360 Nano': 'insta360 Nano',
            'insta360 Air': 'insta360 Air',
            'Gear 360': 'Gear 360 全景相机',
            'theta': 'Ricoh theta',
            'LG 360 CAM': 'LG 360 CAM',
            'insta360 One': 'insta360 One'
        }
        self.today = datetime.datetime.now().strftime('%Y-%m-%d')

    def main(self):
        result = []
        for product in self.products:
            self.commodityList = []
            self.start(self.products[product])
            self.distinct()
            sales = self.getTotalComments()
            temp = {'commodity': product, 'jd_total_sales': sales, 'date': self.today}
            print temp
            result.append(temp)
        jsonResult = json.dumps(result)
        print jsonResult
        return jsonResult

    def start(self, product):
        count = 1
        while (True):
            form_data = {
                '_format_': 'json',
                'stock': 0,
                'sort': '',
                'keyword': product,
                'page': count
            }
            req = requests.post(self.url,params=form_data)
            page = req.text
            data = json.loads(page)
            value = data['value']
            data = json.loads(value)
            ware_info = data['wareList']
            try:
                ware_list = ware_info['wareList']
            except:
                break
            count += 1
            for item in ware_list:
                name = item['wname']
                price = float(item['jdPrice'])
                comment = int(item['totalCount'])
                id = item['wareId']
                good_rate = item['good']
                commodity = Commodity(name, price, comment, id, good_rate)
                self.commodityList.append(commodity)

    def getTotalComments(self):
        totalComments = 0
        for commodity in self.commodityList:
            totalComments += commodity.comment
        return totalComments

    def distinct(self):
        i = 0
        s = set()
        id_set = set()
        while i < len(self.commodityList):
            comment = self.commodityList[i].comment
            id= self.commodityList[i].id
            good_rate = self.commodityList[i].good_rate
            mark = str(comment) + good_rate
            if id in id_set:
                del self.commodityList[i]
                continue
            else:
                id_set.add(id)
            if not mark in s:
                s.add(mark)
            else:
                del self.commodityList[i]
                i -= 1
            i += 1

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')
    jd = JDCrawler()
    jd.main()
