from youku_crawler import get_videos_info as get_youku_videos
from tencent_crawler import get_videos_info as get_tencent_videos
from iqiyi_crawler import get_videos_info as get_iqiyi_videos

def main():
    platform = ['youku', 'tencent', 'iqiyi']
    result = []
    for i in platform:
        res = []
        if i == 'youku':
            res = get_youku_videos()
        elif i == 'tencent':
            res = get_tencent_videos()
        elif i == 'iqiyi':
            res = get_iqiyi_videos()
        result.extend(res)
    return result

if __name__ == "__main__":
    main()
