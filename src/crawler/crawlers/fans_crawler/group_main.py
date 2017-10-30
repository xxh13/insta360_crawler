import datetime

from fb_crawler import get_group_members_by_api as get_fb_group_by_api
# from fb_group_crawler import FbGroupCrawler
def main():
    fb_group = {
        'Insta360 Community': '474514739424333',
        'Insta360 Air Users on Facebook': '1214211688674519',
        'Facebook 360 Live Community': '207817373036253',
        'Facebook Live 360': '1278909362190845',
        'Insta360 (Japanese)': '1909394772625898',
        'Insta360 One Community': '1408383872584870'
    }
    fb_group1 = {
        'Nikon Keymission 360': '1097354146949633',
        '360 Showroom': '978973148827899',
        'Garmin Virb 360 users and fans': '1424515127629162',
        '360 VR Camera Users Community': '927762980666414',
        '360 Cameras group any brand': '1569301146443418',
        'Mijia 360 cam': '387319578329834',
        'Ricoh THETA Users': '1421540578064134'
    }
    result = []
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    # c = FbGroupCrawler()
    for name in fb_group:
        try:
            fans = get_fb_group_by_api(fb_group[name])
            temp = {'platform': 'facebook', 'group_id':fb_group[name],'group_name': name,'member_count': fans, 'date': today, 'is_native': 1}
            result.append(temp)
        except:
            print name
    for name in fb_group1:
        try:
            fans = get_fb_group_by_api(fb_group1[name])
            temp = {'platform': 'facebook', 'group_id':fb_group1[name],'group_name': name,'member_count': fans, 'date': today, 'is_native': 0}
            result.append(temp)
        except:
            print name
    # c.shutdown()
    return result


if __name__ == "__main__":
    main()
