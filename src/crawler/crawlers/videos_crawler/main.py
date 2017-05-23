from youku_crawler import get_videos_info as get_youku_videos
from tencent_crawler import get_videos_info as get_tencent_videos

def main():
    platform = ['youku', 'tencent']
    result = []
    for i in platform:
        res = []
        if i == 'youku':
            res = get_youku_videos()
        elif i == 'tencent':
            res = get_tencent_videos()
        result.extend(res)
    return result

if __name__ == "__main__":
    main()
