# -*- coding: UTF-8 -*-
import sys
import json
import urllib2
import datetime
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding("utf-8")

def get_by_html():
    url = 'http://v.qq.com/vplus/insta360/videos'
    response = urllib2.urlopen(url)
    page = response.read()
    soup = BeautifulSoup(page, 'html.parser')
    total_count = 0
    for linebreak in soup.find_all('br'):
        linebreak.extract()
    div = soup.find('ul',id='videolst_cont')
    list = div.find_all('li',class_='list_item')
    today = datetime.datetime.now()
    for li in list:
        create_time = li.find('span', class_='figure_info_time').text
        try:
            create_time = datetime.datetime.strptime(create_time, "%Y-%m-%d")
            delta = (today - create_time).days
            if delta > 31:
                break
        except:
            pass
        temp = li.find('span',class_='info_inner').text
        if '万' in temp:
            temp = temp[:-1]
            temp = float(temp)
            temp *= 10000
        view_count = int(temp)
        total_count += view_count
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    result = {
        'platform': '腾讯视频',
        'date': today,
        'view': total_count,
        'comment': 0,
        'like': 0,
        'share': 0,
        'dislike': 0,
    }
    jsonResult = json.dumps(result)
    print  jsonResult
    return jsonResult

if __name__ == '__main__':
    get_by_html()
