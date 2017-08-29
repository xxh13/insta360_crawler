# -*- coding: UTF-8 -*-
import time
import re
import sys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
reload(sys)
sys.setdefaultencoding("utf-8")

class FbGroupCrawler:
    def __init__(self):
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'
        headers = {'User-Agent': user_agent}
        cap = webdriver.DesiredCapabilities.PHANTOMJS
        cap["phantomjs.page.settings.resourceTimeout"] = 1000
        cap["phantomjs.page.settings.loadImages"] = False
        cap["phantomjs.page.settings.localToRemoteUrlAccessEnabled"] = True
        cap["userAgent"] = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0"
        cap["XSSAuditingEnabled"] = True
        # driver = webdriver.PhantomJS(desired_capabilities=cap,
        #                                   service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any',
        #                                                 '--web-security=true'])
        self.driver = webdriver.Chrome()
        self.driver.get('https://www.facebook.com/')
        element = self.driver.find_element_by_id('email')
        element.send_keys('15850786305')
        element = self.driver.find_element_by_id('pass')
        element.send_keys('klqbtnsns123')
        element = self.driver.find_element_by_id('loginbutton')
        element.click()
        time.sleep(10)

    def get_group_members(self, group_id):
        url = 'https://www.facebook.com/groups/' + str(group_id)

        self.driver.get(url)
        wait = WebDriverWait(self.driver, 20)
        temp = wait.until(lambda x: x.find_element_by_id('count_text').text)
        pattern = re.compile(u"(.{0,10}) 位成员", re.S)
        items = re.findall(pattern, temp)
        temp = items[0]
        fans = temp.replace(',', '')
        fans = int(fans)
        print fans
        return fans

    def shutdown(self):
        self.driver.quit()

if __name__ == '__main__':
    c = FbGroupCrawler()
    c.get_group_members(474514739424333)