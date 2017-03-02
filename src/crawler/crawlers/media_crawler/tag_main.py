import datetime
import json

from instagram_crawler import get_tag as get_instagram_count

def main():
    platforms = ['instagram']
    tags = ['insta360']
    result = []
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    for platform in platforms:
        for tag in tags:
            count = 0
            if platform == 'instagram':
                count = get_instagram_count(tag)

            temp = {'platform': platform, 'count': count, 'tag':tag, 'date': today}
            result.append(temp)
    jsonResult = json.dumps(result)
    print  jsonResult
    return jsonResult


if __name__ == "__main__":
    main()
