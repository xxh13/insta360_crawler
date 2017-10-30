import datetime
import json

from fb_crawler import get_by_api as get_fb
from weibo_crawler_new import SinaCrawler
from twitter_crawler import get_by_api as get_twitter
from youtube_crawler import YoutubeCrawler
from youku_crawler import get_by_api as get_youku
from weixin_crawler_new import get_by_request as get_weixin
from instagram_crawler import get_by_api as get_instagram
from tencent_crawler import get_by_html as get_tencent

def get_media_platform(is_native):
    if is_native:
        return [
            'youku',
            'weixin',
            'tencent'
        ]
    else:
        return [
            'weibo',
            'youtube',
            'facebook',
            'twitter',
            'instagram'
        ]
def main(is_native):
    platform = get_media_platform(is_native)
    result = []
    for i in platform:
        data = '{}'

        if i == 'facebook':
            data = get_fb()
        elif i == 'weibo':
            c = SinaCrawler()
            data = c.main()
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
        elif i == 'tencent':
            data = get_tencent()

        data = json.loads(data)
        result.append(data)
    jsonResult = json.dumps(result)
    print  jsonResult
    return jsonResult


if __name__ == "__main__":
    main(True)
