# -*- coding: UTF-8 -*-
'''
官方接口
'''
import urllib2
import requests
import json
import time
from bs4 import BeautifulSoup
import re
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
app_id = '143580116255494'
app_secret = '62772cd2ae4727853b36d722fcb9e43d'
# app_id = '1586202924770913'
# app_secret = '2232dc879a06f476e6b8af45d256a3c7'
# app_id = '163680667532581'
# app_secret = '7f5cedfb05643f115af57a6f120fd213'
# app_id = '1598022290502419'
# app_secret = 'f0fc5a210b5531987cbc671a6c3d864f'
access_token = app_id + '|' + app_secret
def get_by_api(username='Insta360Official'):
    url = 'https://graph.facebook.com/' + username + '/?fields=fan_count&access_token=' + access_token
    headers = {}
    headers['Host'] = 'graph.facebook.com'
    headers['Connection'] = 'keep-alive'
    headers['Upgrade-Insecure-Requests'] = '1'
    headers['Cache-Control'] = 'max-age=0'

    # request = urllib2.Request(url = url, headers = headers)
    # response = urllib2.urlopen(request)
    # page = response.read()
    response = requests.get(url=url,headers=headers, verify=False)
    page = response.text
    print page
    jsonData = json.loads(page, encoding="utf-8")
    fans = jsonData['fan_count']
    print fans
    return fans

def get_group_members(group_id):
    url = 'https://www.facebook.com/groups/'+ group_id +'/'
    response = urllib2.urlopen(url)
    page = response.read()
    soup = BeautifulSoup(page, 'html.parser')
    content = soup.find('meta', attrs={'name':'description'})['content']
    pattern = re.compile(u"有(.{0,10})位", re.S)
    items = re.findall(pattern, content)
    temp = items[0]
    fans = temp.replace(',','')
    fans = int(fans)
    print fans
    return fans

def get_group_members_by_api(group_id):
    url = 'https://graph.facebook.com/' + group_id + '/members?fields=fan_count&limit=1000&access_token=' + access_token
    headers = {}
    headers['Host'] = 'graph.facebook.com'
    headers['Connection'] = 'keep-alive'
    headers['Upgrade-Insecure-Requests'] = '1'
    headers['Cache-Control'] = 'max-age=0'
    fans = 0
    while(True):
        time.sleep(3)
        # request = urllib2.Request(url, headers=headers)
        # response = urllib2.urlopen(request)
        # page = response.read()
        response = requests.get(url=url, headers=headers, verify=False)
        page = response.text
        jsonData = json.loads(page, encoding="utf-8")
        temp = len(jsonData['data'])
        fans +=temp
        try:
            url = jsonData['paging']['next']
        except:
            break
    print fans
    return fans

if __name__ == "__main__":
    # get_by_api()
    get_group_members_by_api('474514739424333')
    # get_group_members('1278909362190845')