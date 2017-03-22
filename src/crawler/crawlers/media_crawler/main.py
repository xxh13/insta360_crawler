import datetime
import json

from fb_crawler import get_by_api as get_fb
from weibo_crawler import get_by_api as get_sina
from twitter_crawler import get_by_api as get_twitter
from youtube_crawler import YoutubeCrawler
from youku_crawler import get_by_api as get_youku
from weixin_crawler import get_by_request as get_weixin
from instagram_crawler import get_by_api as get_instagram

def main():
    platform = ['facebook', 'twitter', 'youku', 'weixin', 'instagram', 'weibo', 'youtube', 'weibo']
    result = []
    for i in platform:
        data = '{}'

        if i == 'facebook':
            data = get_fb()
        elif i == 'weibo':
            data = get_sina()
        elif i == 'twitter':
            data = get_twitter()
        elif i == 'youtube':
            c = YoutubeCrawler()
            data = c.main()
        elif i == 'youku':
            data = get_youku()
        elif i == 'weixin':
            data = get_weixin()
        elif i == 'instagram':
            data = get_instagram()

        data = json.loads(data)
        result.append(data)
    jsonResult = json.dumps(result)
    print  jsonResult
    return jsonResult


if __name__ == "__main__":
    main()
