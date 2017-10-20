# -*- coding: UTF-8 -*-
'''
淘宝销量	使用urllib2，用正则匹配获取网页源文件中的json数据。
其中除了获取每个产品的当天总销量外，还要获取各个店铺的当天销量
'''
from Commodity import Commodity

import datetime
import time
import urllib2
import json
import re
import sys
import socket

reload(sys)
sys.setdefaultencoding("utf-8")
timeout = 9999
socket.setdefaulttimeout(timeout)


class TaobaoCrawler:
    def __init__(self):
        self.product = 'insta360 Nano'
        self.keyword = self.product.replace(' ', '+')
        self.date = time.strftime('%Y%m%d', time.localtime(time.time()))
        self.url = "https://s.taobao.com/search?q=" + self.keyword + "&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_" + self.date + "&ie=utf8&sort=sale-desc"
        self.commodityList = []
        self.totalPage = 0
        # user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
        cookie = 'miid=8929995663388453206; hng=CN%7Czh-cn%7CCNY; uc3=sg2=VFQmloNtynToEuMeFQKLTZ21PXTH85EtuHZVkHtdn%2FQ%3D&nk2=CNu7fvUK%2FEvBzGe9&id2=UonciUs0wvLz%2Bg%3D%3D&vt3=F8dARHfB55D4ceKVxQg%3D&lg2=UIHiLt3xD8xYTw%3D%3D; uss=W8hhc%2FiL5F3QQxDnorK5%2Bpxtk6UVQTxdX39qSJdTeNa%2FgPPtvy2njhEaqqM%3D; lgc=klqbtnsns123; tracknick=klqbtnsns123; _cc_=VT5L2FSpdA%3D%3D; tg=0; t=df50d2b4a1821ccecb466ada4db35fc8; mt=ci=-1_0; cookie2=31f737050ec6130e8a50270a329f6824; v=0; thw=cn; swfstore=151527; alitrackid=www.taobao.com; lastalitrackid=www.taobao.com; _m_h5_tk=a83b5b9c622408ab9af96c4a8f8ecf3f_1484714010722; _m_h5_tk_enc=77fdcaea2035bb430ad63b125727deed; _tb_token_=7e735e888a7e7; linezing_session=gsi35HL97qLeTfNpudWTOzFV_1484711392594XGpm_1; JSESSIONID=39D91055DEA807D78FB0FA80DE0A63AF; cna=JZgYEL1ENwACAXeJbdPXPixk; uc1=cookie14=UoW%2FWXYeb%2BAHbQ%3D%3D; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; l=AvX1oXyLVgE50p9P9DX54yLahXuvcqmE; isg=AtLSiT6D3hIxcyKNso1DDjwRI5jex9Z96qDZXpwr_gVwr3KphHMmjdjNabxp'
        pragma = 'no-cache'
        cache_control = 'no-cache'
        upgrade_insecure_requests = 1
        self.headers = {'User-Agent': user_agent, 'pragma': pragma, 'cache-control': cache_control, 'upgrade-insecure-requests':upgrade_insecure_requests, 'cookie':cookie}

    def main(self):
        products = ['insta360 Nano', 'insta360 Air', 'Gear 360', 'theta', 'LG 360 CAM', '小米米家全景相机', 'insta360 One']
        result = []
        for product in products:
            self.product = product
            self.keyword = self.product.replace(' ', '+')
            self.url = "https://s.taobao.com/search?q=" + self.keyword + "&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_" + self.date + "&ie=utf8&sort=sale-desc"
            self.commodityList = []
            self.start()
            sales = self.getTotalSales()
            today = datetime.datetime.now().strftime('%Y-%m-%d')
            stores = []
            for commodity in self.commodityList:
                store = {
                    'name': commodity.name,
                    'price': commodity.price,
                    'pay': commodity.pay,
                    'shop_keeper': commodity.shopKeeper,
                    'shop': commodity.shop,
                    'location': commodity.location,
                    'link': commodity.link,
                    'store_id': commodity.id,
                    'sales': commodity.sales,
                    'is_tmall': commodity.isTmall,
                    'date': today,
                    'commodity': product
                }
                stores.append(store)
            temp = {'commodity': product, 'taobao_total_sales': sales, 'date': today, 'stores': stores}
            print temp
            result.append(temp)
        jsonResult = json.dumps(result)
        # print jsonResult
        return jsonResult

    def start(self):
        result = {}
        try:
            request = urllib2.Request(self.url + "&s=0", headers=self.headers)
            response = urllib2.urlopen(request)
            content = response.read()
            pattern = re.compile('g_page_config = {.*?g_srp_loadCss', re.S)
            items = re.findall(pattern, content)
            jsonResult = items[0][16:-19]
            # print jsonResult
            result = json.loads(jsonResult, encoding="utf-8")
            # print result
            try:
                self.totalPage = result['mods']['pager']['data']['totalPage']
            except:
                self.totalPage = 1
            # print self.totalPage
        except urllib2.URLError, e:
            if hasattr(e, "code"):
                print e.code
            if hasattr(e, "reason"):
                print e.reason

        if self.totalPage > 5:  #因为基本上第5页以后，销量都为0了
            self.totalPage = 5
        count = 1
        for i in range(1, self.totalPage + 1):
            if i != 1:
                try:
                    request = urllib2.Request(self.url + "&s=" + str((i - 1) * 44), headers=self.headers)
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
                if shopKeeper != "":
                    self.commodityList.append(commodity)
                # print count
                # commodity.show()
                count += 1
        if self.product == 'insta360 Nano':
            self.filterNano()
        elif self.product == 'insta360 Air':
            self.filterAir()
        elif self.product == 'Gear 360':
            self.filterGear()
        elif self.product == 'theta':
            self.filterTheta()
        elif self.product == 'LG 360 CAM':
            self.filterLG()
        elif self.product == '小米米家全景相机':
            self.filterMi()
        elif self.product == 'insta360 One':
            self.filterOne()
        self.distinct()
        self.getSalesByRequest()
        self.sort()

    def filterNano(self):
        i = 0
        while i < len(self.commodityList):
            name = self.commodityList[i].name.lower()
            price = self.commodityList[i].price
            if ((not ('insta' in name)) or (not ('nano' in name)) or ('gear' in name) or (price < 500) or (
                        price > 1500)):
                del self.commodityList[i]
                i -= 1
            i += 1

    def filterAir(self):
        i = 0
        while i < len(self.commodityList):
            name = self.commodityList[i].name.lower()
            if ((not ('insta' in name)) or (not ('air' in name))):
                del self.commodityList[i]
                i -= 1
            i += 1

    def filterGear(self):
        i = 0
        while i < len(self.commodityList):
            name = self.commodityList[i].name.lower()
            price = self.commodityList[i].price
            if ((not ('gear' in name)) or (not ('360' in name)) or ('insta' in name) or (price < 999) or (
                        price > 10000)):
                del self.commodityList[i]
                i -= 1
            i += 1

    def filterTheta(self):
        i = 0
        while i < len(self.commodityList):
            name = self.commodityList[i].name.lower()
            price = self.commodityList[i].price
            if ((not ('theta' in name)) or (price < 500) or (price > 11000)):
                del self.commodityList[i]
                i -= 1
            i += 1

    def filterLG(self):
        i = 0
        while i < len(self.commodityList):
            name = self.commodityList[i].name.lower()
            price = self.commodityList[i].price
            if (('头盔' in name) or (price < 800) or (price > 7000)):
                del self.commodityList[i]
                i -= 1
            i += 1

    def filterMi(self):
        i = 0
        while i < len(self.commodityList):
            name = self.commodityList[i].name.lower()
            if (not ('小米' in name or '米家' in name) or not ('全景相机') in name):
                del self.commodityList[i]
                i -= 1
            i += 1

    def filterOne(self):
        i = 0
        while i < len(self.commodityList):
            name = self.commodityList[i].name.lower()
            price = self.commodityList[i].price
            if (price < 1000):
                del self.commodityList[i]
                i -= 1
            i += 1


    def getTotalSales(self):
        totalSales = 0
        for commodity in self.commodityList:
            totalSales += commodity.sales
        return totalSales

    #获取销量
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
            url = "http://api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?appKey=12574478&t=1470231466683&sign=373d61685735e4e01e3a8d3593fdbd6c&api=mtop.taobao.detail.getdetail&v=6.0&ttid=2013%40taobao_h5_1.0.0&type=jsonp&dataType=jsonp&callback=mtopjsonp1&data=%7B%22itemNumId%22%3A%22" + str(
                commodity.id) + "%22%2C%22exParams%22%3A%22%7B%5C%22id%5C%22%3A%5C%22" + str(
                commodity.id) + "%5C%22%7D%22%7D"
            request = urllib2.Request(url, headers=headers)
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
            commodity.setSales(int(sales))
            commodity.setShop(shop)
            if count % 40 == 0:
                time.sleep(5)
            count += 1

    #按销量排序
    def sort(self):
        self.commodityList.sort(key=lambda commodity: commodity.sales, reverse=True)

    # 去重
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

if __name__ == "__main__":
    crawler = TaobaoCrawler()
    crawler.main()
