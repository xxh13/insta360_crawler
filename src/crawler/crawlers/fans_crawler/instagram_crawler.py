# -*- coding: UTF-8 -*-
import urllib2
import json
import urllib

def get_by_request():
    username = 'insta360official'
    url = 'https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20html%20where%20url%3D%22https%3A%2F%2Fwww.instagram.com%2F' + username + '%2F%22%20and%20xpath%3D%22%2Fhtml%2Fbody%2Fscript%5B1%5D%22&format=json'
    headers = {}
    headers['Host'] = 'query.yahooapis.com'
    headers['Connection'] = 'keep-alive'
    headers['Origin'] = 'https://livecounts.net'
    headers['Pragma'] = 'no-cache'
    headers['Referer'] = 'https://livecounts.net/instagram/cielni'
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
    request = urllib2.Request(url=url, headers=headers)
    response = urllib2.urlopen(request)
    page = response.read()
    jsonData = json.loads(page, encoding="utf-8")
    content = jsonData['query']['results']['script']['content']
    content = content[21:-1]
    content = json.loads(content, encoding="utf-8")
    fans = content['entry_data']['ProfilePage'][0]['user']['followed_by']['count']
    print fans
    return fans

if __name__ == "__main__":
    get_by_request()
