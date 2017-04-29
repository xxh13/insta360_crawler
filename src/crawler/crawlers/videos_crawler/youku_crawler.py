# -*- coding: UTF-8 -*-
'''
官方接口
最近一个月动态的评论、点赞、踩、浏览总和
'''
import urllib2
import json
import datetime
from django.utils import timezone

client_id = '138c334850478e6b'
def get_videos_info():
    username = 'Insta360'
    url = 'https://openapi.youku.com/v2/videos/by_user.json?client_id=' + client_id + '&user_name=' + username + '&count=50'
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    page_number = 1
    result = []
    while True :
        request = urllib2.Request(url = url + '&page=' + str(page_number))
        page_number += 1
        response = urllib2.urlopen(request)
        page = response.read()
        jsonData = json.loads(page, encoding="utf-8")
        videos = jsonData['videos']
        if len(videos) == 0:
            break
        for item in videos:
            published_time = datetime.datetime.strptime(item['published'], "%Y-%m-%d %H:%M:%S")
            published_time = timezone.make_aware(published_time, timezone.get_current_timezone())
            view = int(item['view_count'])
            dislike= int(item['down_count'])
            like = int(item['up_count'])
            comment = int(item['comment_count'])
            link = item['link']
            title = item['title']
            duration = int(item['duration'])
            thumb = item['bigThumbnail']
            id = item['id']
            temp = {
                'platform': 'youku',
                'video_id': id,
                'title': title,
                'published_time': published_time,
                'view': view,
                'like': like,
                'dislike': dislike,
                'comment': comment,
                'link': link,
                'thumb': thumb,
                'duration': duration,
                'date': today
            }
            result.append(temp)
    return result


if __name__ == '__main__':
    get_videos_info()
