# -*- coding: UTF-8 -*-

import time
import re
import datetime
import json
import sys
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import selenium.webdriver.support.ui as ui
reload(sys)
sys.setdefaultencoding("utf-8")

class SinaCrawler:
    def __init__(self):
        username = '15850786305'  # 输入你的用户名
        password = '11223344'  # 输入你的密码
        self.user_id = 'insta360'
        # 先调用无界面浏览器PhantomJS或Firefox
        cap = webdriver.DesiredCapabilities.PHANTOMJS
        cap["phantomjs.page.settings.resourceTimeout"] = 1000
        cap["phantomjs.page.settings.loadImages"] = False
        cap["phantomjs.page.settings.localToRemoteUrlAccessEnabled"] = True
        cap["userAgent"] = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0"
        cap["XSSAuditingEnabled"] = True
        self.driver = webdriver.PhantomJS(desired_capabilities=cap,
                                          service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any',
                                                        '--web-security=true'])

        # options = webdriver.ChromeOptions()
        # options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
        # self.driver = webdriver.Chrome(chrome_options=options)
        now = time.mktime(datetime.date.today().timetuple())
        self.week_ago = now - (3600 * 24 * 7)
        self.today = datetime.datetime.now().strftime('%Y-%m-%d')
        self.LoginWeibo_m(username, password)

    def LoginWeibo(self, username, password):
        # 输入用户名/密码登录
        print u'准备登陆Weibo.cn网站...'
        self.driver.get("http://www.weibo.com/login.php")
        self.driver.maximize_window()
        wait = WebDriverWait(self.driver, 20)
        try:
            wait.until(lambda x: x.find_element_by_id("loginname"))
        except TimeoutException:
            return

        elem_user = self.driver.find_element_by_id("loginname")
        elem_user.send_keys(username)  # 用户名
        elem_pwd = self.driver.find_element_by_name("password")
        elem_pwd.send_keys(password)  # 密码
        elem_sub = self.driver.find_element_by_xpath("//*[@id='pl_login_form']/div/div[3]/div[6]/a")
        elem_sub.click()  # 点击登陆
        time.sleep(5)
        print u'登陆成功...'

    def LoginWeibo_m(self, username, password):
        # 输入用户名/密码登录
        print u'准备登陆Weibo.cn网站...'
        self.driver.get("https://passport.weibo.cn/signin/login")
        wait = WebDriverWait(self.driver, 20)
        try:
            wait.until(lambda x: x.find_element_by_id("loginName"))
        except TimeoutException:
            return
        time.sleep(10)
        elem_user = self.driver.find_element_by_id("loginName")
        elem_user.send_keys(username)  # 用户名
        elem_pwd = self.driver.find_element_by_id("loginPassword")
        elem_pwd.send_keys(password)  # 密码
        elem_sub = self.driver.find_element_by_id("loginAction")
        elem_sub.click()  # 点击登陆
        time.sleep(10)
        print u'登陆成功...'


    def main(self):
        user_id = self.user_id
        share_total = 0
        like_total = 0
        comment_total = 0
        print u'准备访问个人网站.....'
        self.driver.get("http://weibo.cn/" + user_id)
        print '\n'
        print u'获取微博内容信息'
        num = 1
        while num <= 10:
            url_wb = "http://weibo.cn/" + user_id + "?filter=0&page=" + str(num)
            self.driver.get(url_wb)
            posts = self.driver.find_elements_by_xpath("//div[@class='c']")
            for i in range(0, len(posts)):
                info = posts[i].text
                if (u'设置:皮肤.图片' not in info):
                    str1 = info.split(u" 赞")[-1]
                    like = 0
                    if str1:
                        val1 = re.match(r'\[(.*?)\]', str1).groups()[0]
                        like = val1

                    str2 = info.split(u" 转发")[-1]
                    share = 0
                    if str2:
                        val2 = re.match(r'\[(.*?)\]', str2).groups()[0]
                        share = val2

                    str3 = info.split(u" 评论")[-1]
                    comment = 0
                    if str3:
                        val3 = re.match(r'\[(.*?)\]', str3).groups()[0]
                        comment = val3

                    str4 = info.split(u" 收藏 ")[-1]
                    flag = str4.find(u"来自")
                    temp_time = str4[:(flag - 1)]
                    created_time = self.format_time(temp_time)
                    date = created_time[0:10]
                    temp = time.mktime(time.strptime(date, "%Y-%m-%d"))
                    if temp >= self.week_ago:
                        share_total += int(share)
                        comment_total += int(comment)
                        like_total += int(like)
                    elif u'[置顶]' not in info:
                        num = 11
                        break
                else:
                    break
            num += 1
        self.driver.quit()
        result = {
            'platform': 'weibo',
            'date': self.today,
            'comment': comment_total,
            'like': like_total,
            'share': share_total,
            'dislike': 0,
            'view': 0
        }
        jsonResult = json.dumps(result)
        print  jsonResult
        return jsonResult

    def format_time(self, string):
        now = datetime.datetime.now()
        result = now.strftime('%Y-%m-%d %H:%M:%S')
        if u'分钟前' in string:
            d = int(string[0:1])
            temp = now - datetime.timedelta(minutes= d)
            result =temp.strftime('%Y-%m-%d %H:%M:%S')
        elif u'今天' in string:
            t = string[-5:]
            temp = now.strftime('%Y-%m-%d')
            result = temp + ' ' + t + ':00'
        elif u'月' in string:
            temp = time.strptime(string, "%m月%d日 %H:%M".decode('utf-8'))
            result = str(now.year) + '-' + time.strftime("%m-%d %H:%M:%S", temp)
        elif len(string) == 19:
            result = string
        return result

    def get_tag_count(self, tag):
        url = 'http://huati.weibo.com/k/' + str(tag)
        response = requests.get(url=url, verify=False)
        page = response.text
        pattern = re.compile("var url = \"(http://weibo.com/p/.{50,999}&_from_=huati_topic)\";", re.S)
        items = re.findall(pattern, page)
        url = items[0]
        print url
        self.driver.get(url)
        time.sleep(5)
        self.driver.get(url)
        try:
            wait = WebDriverWait(self.driver, 20)
            temp = wait.until(lambda x: x.find_element_by_xpath("//*[@id='Pl_Third_App__11']/div/div/div[2]/div/ul/li[3]/a/span[1]/em").text)
            pattern = re.compile(u"共(\d+)条", re.S)
            items = re.findall(pattern, temp)
            temp = items[0]
            count = int(temp)
        except TimeoutException:
            count = 0
        print count
        return count

    def shutdown(self):
        self.driver.quit()

if __name__ == '__main__':
    crawler = SinaCrawler()
    crawler.main()
    # crawler.get_tag_count(u'Nano全景相机')
    # crawler.shutdown()
