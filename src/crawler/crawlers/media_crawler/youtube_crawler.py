# -*- coding: UTF-8 -*-
'''
官方接口
最近一个月动态的评论、点赞、踩、浏览总和
'''
import urllib2
import time
import json
import datetime
import requests
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
app_key = 'AIzaSyBg_mtqCgH3mhrTFPVOqDnNeN8wVVO_s5I'
class YoutubeCrawler:
    def __init__(self):
        self.video_ids = []
        self.maxResults = 50
        playlist_id = 'UU3qWcF49rv8VMZO7Vg6kj5w'
        self.list_api = 'https://www.googleapis.com/youtube/v3/playlistItems?maxResults=' + str(self.maxResults) + '&part=snippet&playlistId=' + playlist_id + '&key=' + app_key
        self.info_api = 'https://www.googleapis.com/youtube/v3/videos'
        now = time.mktime(datetime.date.today().timetuple())
        self.week_ago = now - (3600 * 24 * 30)
        self.view_total = 0
        self.like_total = 0
        self.dislike_total = 0
        self.comment_total = 0
    def main(self):
        self.get_video_ids()
        return self.get_videos_info()

    def get_video_ids(self):
        url = self.list_api
        response = requests.get(url=url, verify=False)
        page = response.text
        result = json.loads(page, encoding="utf-8")
        videos = result['items']
        for video in videos:
            self.video_ids.append(video['snippet']['resourceId']['videoId'])

        while(result.has_key('nextPageToken')):
            url = self.list_api + '&pageToken=' + result['nextPageToken']
            request = urllib2.Request(url=url)
            response = urllib2.urlopen(request)
            page = response.read()
            result = json.loads(page, encoding="utf-8")
            videos = result['items']
            for video in videos:
                self.video_ids.append(video['snippet']['resourceId']['videoId'])


    def get_videos_info(self):
        url = self.info_api
        query = ''
        count = 0
        for i in self.video_ids:
            count += 1
            query = query + i + ','
            if count % self.maxResults == 0 or count == len(self.video_ids):
                query = query[:-1]
                results = requests.get(url,
                               params={'id': query, 'maxResults': self.maxResults, 'part': 'snippet,statistics', 'key': app_key}, verify=False)
                page = results.content
                videos = json.loads(page, encoding="utf-8")['items']
                for video in videos:
                    try:
                        like_count = int(video['statistics']['likeCount'])
                    except KeyError:
                        like_count = 0
                    try:
                        dislike_count = int(video['statistics']['dislikeCount'])
                    except KeyError:
                        dislike_count = 0
                    temp = time.mktime(time.strptime(video['snippet']['publishedAt'], "%Y-%m-%dT%H:%M:%S.000Z"))
                    if temp >= self.week_ago:
                        self.dislike_total += dislike_count
                        self.like_total += like_count
                        self.comment_total += int(video['statistics']['commentCount'])
                        self.view_total += int(video['statistics']['viewCount'])
                    query = ''
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        result = {
            'platform': 'youtube',
            'date': today,
            'comment': self.comment_total,
            'like': self.like_total,
            'share': 0,
            'dislike': self.dislike_total,
            'view': self.view_total
        }
        jsonResult = json.dumps(result)
        print  jsonResult
        return jsonResult

def get_tag_count(tag):
    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    yesterday = (today - oneday).strftime('%Y-%m-%d')
    date = yesterday + 'T00:00:00Z'
    url = 'https://www.googleapis.com/youtube/v3/search?part=snippet&key=' + app_key + '&q=%23' + tag + '&publishedAfter=' + date
    # request = urllib2.Request(url=url)
    # response = urllib2.urlopen(request)
    # page = response.read()
    response = requests.get(url=url, verify=False)
    page = response.text
    data = json.loads(page, encoding="utf-8")
    count = data['pageInfo']['totalResults']
    print count
    return count

if __name__ == "__main__":
    c = YoutubeCrawler()
    c.main()
    # get_tag_count('insta360')