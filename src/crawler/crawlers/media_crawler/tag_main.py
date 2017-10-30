# -*- coding: UTF-8 -*-
import datetime
import json

from instagram_crawler import get_tag_count as get_instagram_count
from twitter_crawler import get_tag_count as get_twitter_count
from youtube_crawler import get_tag_count as get_youtube_count
from youku_crawler import get_tag_count as get_youku_count
from weibo_crawler_new import SinaCrawler

def get_tag_platform(is_native):
    if is_native:
        return [
            'youku'
        ]
    else:
        return [
            'twitter',
            'youtube',
            'instagram'
        ]

def main(is_native):
    platforms = get_tag_platform(is_native)
    tags = ['insta360']
    result = []
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    for platform in platforms:
        for tag in tags:
            count = 0
            if platform == 'instagram':
                count = get_instagram_count(tag)
            elif platform == 'twitter':
                count = get_twitter_count(tag)
            elif platform == 'youtube':
                count = get_youtube_count(tag)
            elif platform == 'youku':
                count = get_youku_count(tag)
            elif platform == 'weibo':
                count = get_youku_count(tag)
            temp = {'platform': platform, 'count': count, 'tag':tag, 'date': today}
            result.append(temp)
    # weibo_tags = [u'Nano全景相机']
    # c = SinaCrawler()
    # for tag in weibo_tags:
    #     count = c.get_tag_count(tag)
    #     temp = {'platform': 'weibo', 'count': count, 'tag':tag, 'date': today}
    #     result.append(temp)
    # c.shutdown()
    jsonResult = json.dumps(result)
    print  jsonResult
    return jsonResult


if __name__ == "__main__":
    main(True)
