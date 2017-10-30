import datetime
import json

from fb_crawler import get_by_api as get_fb_fans
from weibo_crawler import get_by_request as get_sina_fans
from twitter_crawler import get_by_request as get_twitter_fans
from youtube_crawler import get_by_api as get_youtube_fans
from youku_crawler import get_by_api as get_youku_fans
from weixin_crawler import get_by_api as get_weixin_fans
from instagram_crawler import get_by_request as get_instagram_fans
from fb_crawler import get_group_members as get_fb_group
from fb_crawler import get_group_members_by_api as get_fb_group_by_api

def get_fan_platform(is_native):
    if is_native:
        return [
            'youku',
            'weixin'
        ]
    else:
        return [
            'facebook',
            'twitter',
            'youtube',
            'instagram',
            'weibo',
        ]



def main(is_native):
    platform = get_fan_platform(is_native)

    twitter_users = [
        'insta360japan'
    ]

    result = []
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    for i in platform:
        fans = 0
        if i == 'facebook':
            fans = get_fb_fans()
        if i == 'weibo':
            fans = get_sina_fans()
        elif i == 'twitter':
            fans = get_twitter_fans()
        elif i == 'youtube':
            fans = get_youtube_fans()
        elif i == 'youku':
            fans = get_youku_fans()
        elif i == 'weixin':
            fans = get_weixin_fans()
        elif i == 'instagram':
            fans = get_instagram_fans()
        temp = {'platform': i, 'fans': fans, 'date': today}
        result.append(temp)

    if not is_native:
        for user in twitter_users:
            fans = get_twitter_fans(user)
            temp = {'platform': 'twitte' + '@' + user, 'fans': fans, 'date': today}
            result.append(temp)


    jsonResult = json.dumps(result)
    print  jsonResult
    return jsonResult


if __name__ == "__main__":
    main(True)
