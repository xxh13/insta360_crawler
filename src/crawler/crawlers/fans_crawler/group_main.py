import datetime

# from fb_crawler import get_group_members_by_api as get_fb_group_by_api
from fb_group_crawler import FbGroupCrawler
def main():
    fb_group = {
        'Insta360 Community': '474514739424333',
        'Insta360 Air Users on Facebook': '1214211688674519',
        'Facebook 360 Live Community': '207817373036253',
        'Insta360 Pro Feedback Group': '1277002085710268',
        'Insta360 Pro Europe': '730257723823125',
        'Insta360 (Japanese)': '1909394772625898'
    }
    fb_group1 = {
        '360 VR Video Professionals': '1446468078916774',
        'Ricoh THETA Users on Facebook': '1421540578064134',
        'Nikon Keymission 360': '1097354146949633',
        '360 Showroom': '978973148827899',
        'Garmin Virb 360 users and fans': '1424515127629162',
        '360 Panoramic Photographers on Facebook': '146240618753391',
        'VR inside - VR AR MR': '1781579258758436',
        '360 VR Camera Users Community': '927762980666414',
        '360 Cameras group any brand': '1569301146443418',
        'Facebook 360 Community': '241193586214590'
    }
    result = []
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    c = FbGroupCrawler()
    for name in fb_group:
        fans = c.get_group_members(fb_group[name])
        temp = {'platform': 'facebook', 'group_id':fb_group[name],'group_name': name,'member_count': fans, 'date': today, 'is_native': 1}
        result.append(temp)
    for name in fb_group1:
        fans = c.get_group_members(fb_group1[name])
        temp = {'platform': 'facebook', 'group_id':fb_group1[name],'group_name': name,'member_count': fans, 'date': today, 'is_native': 0}
        result.append(temp)
    c.shutdown()
    return result


if __name__ == "__main__":
    main()
