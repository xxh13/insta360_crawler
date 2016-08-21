#-*- coding: UTF-8 -*-
import socket

timeout = 9999
socket.setdefaulttimeout(timeout)
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
import datetime
import time
import urllib2
import json
from Commodity import Commodity
import re


class TaobaoCrawler:
        def __init__(self):
            self.product = 'insta360 Nano'
            self.keyword = self.product.replace(' ','+')
            self.date = time.strftime('%Y%m%d', time.localtime(time.time()))
            self.url = "https://s.taobao.com/search?q="+self.keyword+"&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_"+self.date+"&ie=utf8"+"sort=sale-desc"
            self.commodityList = []
            self.totalPage = 0
            user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'
            self.headers = {'User-Agent': user_agent}

        def main(self):
            products = ['insta360 Nano', 'Gear 360', 'theta', 'LG 360 CAM']
            result = []
            for product in products:
                self.product = product
                self.keyword = self.product.replace(' ', '+')
                self.url = "https://s.taobao.com/search?q=" + self.keyword + "&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_" + self.date + "&ie=utf8" + "sort=sale-desc"
                self.commodityList = []
                self.start()
                sales = self.getTotalSales()
                today = datetime.datetime.now().strftime('%Y-%m-%d')
                temp = {'commodity': product, 'taobao_total_sales': sales, 'date':today}
                result.append(temp)
            jsonResult = json.dumps(result)
            return jsonResult

        def start(self):
            result = {}
            try:
                request = urllib2.Request(self.url+"&s=0", headers = self.headers)
                response = urllib2.urlopen(request)
                content = response.read()
                pattern = re.compile('g_page_config = {.*?g_srp_loadCss', re.S)
                items = re.findall(pattern, content)
                jsonResult = items[0][16:-19]
                # print jsonResult
                result = json.loads(jsonResult, encoding="utf-8")
                # print result
                self.totalPage = result['mods']['pager']['data']['totalPage']
                # print self.totalPage
            except urllib2.URLError, e:
                if hasattr(e, "code"):
                    print e.code
                if hasattr(e, "reason"):
                    print e.reason

            if self.totalPage > 3 :
                self.totalPage = 3
            count = 1
            for i in range(1, self.totalPage+1):
                # print "page ",i ,":"
                if i != 1:
                    try:
                        request = urllib2.Request(self.url+"&s="+str((i-1)*44), headers=self.headers)
                        response = urllib2.urlopen(request)
                        content = response.read()
                        pattern = re.compile('g_page_config = {.*?g_srp_loadCss', re.S)
                        items = re.findall(pattern, content)
                        jsonResult = items[0][16:-19]
                        # print jsonResult
                        result = json.loads(jsonResult, encoding="utf-8")
                    except urllib2.URLError, e:
                        if hasattr(e, "code"):
                            print e.code
                        if hasattr(e, "reason"):
                            print e.reason
                elements = result['mods']['itemlist']['data']['auctions']
                for element in elements:
                    name = element['raw_title']
                    price = float(element['view_price'])
                    pay = int(element['view_sales'][:-3])
                    shopKeeper = element['nick']
                    location = element['item_loc']
                    link = 'https:' + element['detail_url']
                    id = str(element['nid'])
                    commodity = Commodity(name, price, pay, shopKeeper, location, link, id)
                    if "tmall" in link or "click.simba" in link:
                        commodity.setIsTmall(True)
                    if shopKeeper!="":
                        self.commodityList.append(commodity)
                    # print count
                    # commodity.show()
                    count += 1
            if self.product =='insta360 Nano':
                self.filterNano()
            elif self.product =='Gear 360':
                self.filterGear()
            elif self.product =='theta':
                self.filterTheta()
            elif self.product =='LG 360 CAM':
                self.filterLG()
            self.distinct()
            self.getSalesByRequest()
            # self.sort()
            # self.showList()
            # self.save()

        def filterNano(self):
            i = 0
            while i < len(self.commodityList):
                name = self.commodityList[i].name.lower()
                price = self.commodityList[i].price
                if((not ('insta' in name)) or (not ('nano' in name)) or ('gear' in name) or (price < 100) or (price >2317)):
                    del self.commodityList[i]
                    i -= 1
                i += 1

        def distinct(self):
            i = 0
            s = set()
            while i < len(self.commodityList):
                id = self.commodityList[i].id
                if not id in s:
                    s.add(id)
                else:
                    del self.commodityList[i]
                    i -= 1
                i += 1

        def filterGear(self):
            i = 0
            while i < len(self.commodityList):
                name = self.commodityList[i].name.lower()
                price = self.commodityList[i].price
                if((not ('gear' in name)) or (not ('360' in name)) or ('insta' in name) or (price < 999) or (price >10000)):
                    del self.commodityList[i]
                    i -= 1
                i += 1

        def filterTheta(self):
            i = 0
            while i < len(self.commodityList):
                name = self.commodityList[i].name.lower()
                price = self.commodityList[i].price
                if((not ('theta' in name)) or (price < 500) or (price >11000)):
                    del self.commodityList[i]
                    i -= 1
                i += 1

        def filterLG(self):
            i = 0
            while i < len(self.commodityList):
                name = self.commodityList[i].name.lower()
                price = self.commodityList[i].price
                if(('头盔' in name) or (price < 800) or (price >7000)):
                    del self.commodityList[i]
                    i -= 1
                i += 1

        def showList(self):
            count = 1
            for commodity in self.commodityList:
                # print count
                commodity.show()
                count += 1

        def getTotalSales(self):
            totalSales = 0
            for commodity in self.commodityList:
                totalSales += commodity.sales
            return totalSales

        def save(self):
            file = open(self.product+'.txt','w')
            string = ''
            count = 1
            totalSales = 0
            totalPrice = 0.0
            for commodity in self.commodityList:
                source = "淘宝"
                if commodity.isTmall == True:
                    source = "天猫"
                string = string + str(count) + '\n'
                string = string + '商品名: ' + commodity.name + '\n' + '价格: ' + str(commodity.price) + ' 元' + '\n' + '销量: ' + str(commodity.sales) + '\n' + '收货: ' + str(commodity.pay) + '\n' + '店铺: ' + commodity.shop + '\n' + '掌柜: ' + commodity.shopKeeper + '\n' + '地区: ' + commodity.location + '\n' + '链接: ' + commodity.link + '\n' + 'ID: ' + commodity.id + '\n' + '来源: ' + source + '\n' + '\n'
                count += 1
                totalSales += commodity.sales
                totalPrice += commodity.price
            averagePrice = round(totalPrice/count, 2)
            string = '产品： '+ self.product + '\n' + '总销售量: ' + str(totalSales) + '\n' + '平均价格: ' + str(averagePrice) + ' 元' + '\n' + '\n' + '\n' + string
            file.write(string)
            file.close()

        def getSalesByRequest(self):
            headers = {}
            headers['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0"
            headers[
                'Cookie'] = "l=Atrac3Qq0K3ugb7iycBh/IYtCov8C17l; isg=Av__gx9WlJezgpC0ccEJCtlXjdNC0_PlUaOKeZHMm671oB8imbTj1n22lOqw; cna=m6slEI92cRUCATo8eHdZ2zu1; _m_h5_tk=8cf47b4ebce635952707782c7d500872_1470233775411; _m_h5_tk_enc=fefa6e767a6e9648f172fff8d492d66a; thw=cn; t=994a0942d22e2452f893be72b33881a6; mt=ci%3D-1_0; supportWebp=false"
            headers['Host'] = "api.m.taobao.com"
            headers['Accept'] = "*/*"
            headers['Accept-Language'] = "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3"
            headers['X-Requested-With'] = 'XMLHttpRequest'
            headers['Connection'] = 'keep-alive'
            count = 1
            for commodity in self.commodityList:
                shop = commodity.shopKeeper
                headers['Referer'] = "http://h5.m.taobao.com/awp/core/detail.htm?id=" + str(commodity.id)
                url = "http://api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?appKey=12574478&t=1470231466683&sign=373d61685735e4e01e3a8d3593fdbd6c&api=mtop.taobao.detail.getdetail&v=6.0&ttid=2013%40taobao_h5_1.0.0&type=jsonp&dataType=jsonp&callback=mtopjsonp1&data=%7B%22itemNumId%22%3A%22" + str(commodity.id) + "%22%2C%22exParams%22%3A%22%7B%5C%22id%5C%22%3A%5C%22"+ str(commodity.id) +"%5C%22%7D%22%7D"
                request = urllib2.Request(url,headers=headers)
                try:
                    response = urllib2.urlopen(request)
                    jsonData = response.read()
                    # print "result", jsonData
                    result = json.loads(jsonData[11:-1], encoding="utf-8")
                    result1 = json.loads(result['data']['apiStack'][0]['value'], encoding="utf-8")
                    sales = result1['item']['sellCount']
                    # print result['data']['seller']['shopName']
                    shop = result['data']['seller']['shopName']
                except:
                    sales = 0
                    # print "Fail",commodity.id
                # print sales
                commodity.setSales(int(sales))
                commodity.setShop(shop)
                if count%40 == 0:
                    time.sleep(5)
                count += 1

        def sort(self):
            self.commodityList.sort(key = lambda commodity: commodity.sales, reverse=True)
