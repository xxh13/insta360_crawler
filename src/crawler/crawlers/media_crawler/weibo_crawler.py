# -*- coding: UTF-8 -*-
'''
官方接口（只能显示最近六条）
最近6条动态的评论、点赞、转发总和
'''
import urllib
import urllib2
import datetime
import time
import json
import re
import requests
import base64


def get_by_api():
    url = 'https://api.weibo.com/2/statuses/user_timeline.json?page=1'
    username = 'newmedia@vzhibo.tv'
    password = 'lanfeng123'
    value = {}
    value['trim_user'] = '1'
    value['count'] = '100'
    value['source'] = '218121934'
    data = urllib.urlencode(value)
    base64string = base64.encodestring(
        '%s:%s' % (username, password))[:-1]  # 注意哦，这里最后会自动添加一个\n
    authheader = "Basic %s" % base64string
    header = {}
    header['Authorization'] = authheader
    now = time.mktime(datetime.date.today().timetuple())
    week_ago = now - (3600 * 24 * 7)
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    share_total = 0
    like_total = 0
    comment_total = 0
    results = requests.get(url=url, params=data, headers=header, verify=False)
    page = results.content
    print page
    jsonData = json.loads(page, encoding="utf-8")
    data = jsonData['statuses']
    for item in data:
        temp = time.mktime(time.strptime(item['created_at'], "%a %b %d %H:%M:%S +0800 %Y"))
        if temp >= week_ago:
            share_total += int(item['reposts_count'])
            like_total += int(item['attitudes_count'])
            comment_total += int(item['comments_count'])
    result = {
        'platform': 'weibo',
        'date': today,
        'comment': comment_total,
        'like': like_total,
        'share': share_total,
        'dislike': 0,
        'view': 0
    }
    jsonResult = json.dumps(result)
    print  jsonResult
    return jsonResult

def get_tag_count(tag):
    from selenium import webdriver
    from selenium.common.exceptions import TimeoutException
    from selenium.webdriver.support.ui import WebDriverWait
    cap = webdriver.DesiredCapabilities.PHANTOMJS
    cap["phantomjs.page.settings.resourceTimeout"] = 1000
    cap["phantomjs.page.settings.loadImages"] = False
    cap["phantomjs.page.settings.localToRemoteUrlAccessEnabled"] = True
    cap["userAgent"] = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0"
    cap["XSSAuditingEnabled"] = True
    driver = webdriver.PhantomJS(desired_capabilities=cap,service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any',
                                               '--web-security=true'])
    url = 'http://huati.weibo.com/k/' + str(tag)
    request = urllib2.Request(url=url)
    response = urllib2.urlopen(request)
    page = response.read()
    pattern = re.compile("var url = \"(http://weibo.com/p/.{10,50}&_from_=huati_topic)\";", re.S)
    items = re.findall(pattern, page)
    url = items[0]
    print url
    driver.get(url)
    print driver.page_source
    try:
        wait = WebDriverWait(driver, 10)
        count = int(
            wait.until(lambda x: x.find_element_by_xpath("//*[@id='Pl_Core_T8CustomTriColumn__12']/div[2]/div[1]/div/div/table/tbody/tr/td[2]/strong").text))
    except TimeoutException:
        count = 0
    driver.quit()
    print count
    # header = {}
    # header['host'] = 'www.weibo.com'
    # header['user-agent'] = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    # request = urllib2.Request(url=url, headers=header)
    # response = urllib2.urlopen(request)
    # page = response.read()
    # print page

if __name__ == "__main__":
    get_by_api()
    # get_tag_count('insta360')