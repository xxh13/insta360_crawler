#-*- coding: UTF-8 -*-
import socket, sys
timeout = 99999999
socket.setdefaulttimeout(timeout)
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
import datetime
import time
import urllib2
import json
from Commodity import Commodity
import re


class JDCrawler:
        def __init__(self):
            self.product = 'insta360 Nano'
            self.keyword = self.product.replace(' ','+')
            self.date = time.strftime('%Y%m%d', time.localtime(time.time()))
            self.url = ""
            self.commodityList = []
            self.totalPage = 0
            user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'
            self.headers = {'User-Agent': user_agent}
            self.cap = webdriver.DesiredCapabilities.PHANTOMJS
            self.cap["phantomjs.page.settings.resourceTimeout"] = 1000
            self.cap["phantomjs.page.settings.loadImages"] = False
            self.cap["phantomjs.page.settings.localToRemoteUrlAccessEnabled"] = True
            self.cap["userAgent"] = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0"
            self.cap["XSSAuditingEnabled"] = True
            self.driver = webdriver.PhantomJS(desired_capabilities=self.cap)
            # self.driver = webdriver.Chrome()
        def main(self):
            products = ['insta360 Nano', 'Gear 360', 'theta', 'LG 360 CAM']
            result = []
            for product in products:
                self.product = product
                self.keyword = self.product.replace(' ', '+')
                self.url = "http://search.jd.com/Search?keyword=" + self.keyword + "&enc=utf-8&psort=4"
                self.commodityList = []
                self.start()
                sales = self.getTotalComments()
                today = datetime.datetime.now().strftime('%Y-%m-%d')
                temp = {'commodity': product, 'jd_total_sales': sales, 'date':today}
                result.append(temp)
            self.driver.quit()
            jsonResult = json.dumps(result)
            # print jsonResult
            return jsonResult

        def start(self):
            print 'init'
            self.driver.get(self.url + "&page=1")
            print 'load...'
            wait = WebDriverWait(self.driver, 10)
            try:
                self.totalPage = int(
                    wait.until(lambda x: x.find_element_by_xpath("//*[@id='J_bottomPage']/span[2]/em[1]/b").text))
            except TimeoutException:
                self.totalPage = 1
            # print "totalPage: ", self.totalPage
            if self.totalPage > 5:
                self.totalPage = 5
            count = 1
            for i in range(1, self.totalPage + 1):
                # print "page ", i, ":"
                if i != 1:
                    self.driver.get(self.url + "&page=" + str((i - 1)*2+1))
                warp = wait.until(lambda x: x.find_elements_by_class_name("gl-warp"))[0]
                elements = warp.find_elements_by_class_name('gl-item')
                for element in elements:
                    name = element.find_element_by_xpath("div/div[@class='p-name p-name-type-2']/a/em").text
                    price = float(element.find_element_by_xpath("div/div[@class='p-price']/strong/i").text)
                    temp = element.find_element_by_xpath("div/div[@class='p-commit']/strong/a").text
                    temp = temp.replace('+','')
                    temp = temp.replace('万', '')
                    comment = int(temp)
                    link = element.find_element_by_xpath("div/div[@class='p-img']/a").get_attribute("href")
                    id = element.get_attribute("data-sku")
                    commodity = Commodity(name, price, comment, link, id)
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
                if((not ('gear' in name)) or (not ('360' in name)) or (price < 999) or (price >10000)):
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

        def getTotalComments(self):
            totalComments = 0
            for commodity in self.commodityList:
                totalComments += commodity.comment
            return totalComments

        def sort(self):
            self.commodityList.sort(key = lambda commodity: commodity.sales, reverse=True)

#
# if __name__ == "__main__":
#     reload(sys)
#     sys.setdefaultencoding('utf-8')
#     jd = JDCrawler()
#     jd.main()
