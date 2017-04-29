# -*- coding: UTF-8 -*-
'''
get_google_index()
get_fans()
get_media_data()
需要翻墙
'''
from __future__ import absolute_import
from celery import shared_task
from celery.utils.log import get_task_logger
from django.db.models import Sum
from .models import UseCondition
from .models import SearchIndex
from .models import GoogleIndex
from .models import CompetitorSales
from .models import UserDistribution
from .models import ErrorCondition
from .models import ShareChannel
from .models import ShareMode
from .models import ShareCount
from .models import TakeCount
from .models import MediaFan
from .models import MediaData
from .models import MediaTag
from .models import TaobaoDetail
from .models import GlobalElectronicSales
from .models import Meltwater
from .models import YoukuData
from .crawlers.umeng.UmengCrawler import UmengCrawler
from .crawlers.taobao.TaobaoCrawler import TaobaoCrawler
from .crawlers.jd.JDmobileCrawler import JDCrawler
from .crawlers.meltwater.MeltwaterCrawler import MeltwaterCrawler
from .crawlers.baidu_index.main import *
from .crawlers.youku_crawler.youku_crawler import get_videos_info
from .crawlers.amazon.amazon_crawler import main as amanzon_crawler
from .crawlers.google_index.google_trends import google_index
from .crawlers.fans_crawler.main import main as fans_crawler
from .crawlers.media_crawler.main import main as media_crawler
from .crawlers.media_crawler.tag_main import main as tag_crawler
from .util.admin import password_updater

import datetime
import time
import urllib2
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

logger = get_task_logger(__name__)

#用户概况 对应model： UseCondition
@shared_task
def get_use_condition():
    today = datetime.datetime.today()
    end_date = today.strftime('%Y-%m-%d')
    start_date = (today - datetime.timedelta(days=6)).strftime('%Y-%m-%d')
    result = '[]'
    count = 0
    while True:
        try:
            count += 1
            crawler = UmengCrawler()
            result = crawler.getUseCondition(start_date, end_date)
            break
        except:
            print 'error'
            if count >= 3:
                break
            time.sleep(5)
    data = json.loads(result)
    for item in data:
        UseCondition.objects.update_or_create(date=item['date'], product=item['product'], defaults=item)
    return 'Finished.'

#百度指数 对应model： SearchIndex
@shared_task
def get_baidu_index():
    today = datetime.datetime.today()
    end_date = today.strftime('%Y-%m-%d')
    start_date = (today - datetime.timedelta(days=6)).strftime('%Y-%m-%d')
    result = '[]'
    count = 0
    while True:
        try:
            count += 1
            result = baidu_index(start_date, end_date)
            break
        except:
            print 'error'
            if count >= 3:
                break
            time.sleep(5)
    data = json.loads(result)
    for item in data:
        SearchIndex.objects.update_or_create(date=item['date'], key=item['key'], defaults=item)
    return 'Finished.'

#谷歌指数 对应model： GoogleIndex    （需要翻墙）
@shared_task
def get_google_index():
    result = '[]'
    count = 0
    while True:
        try:
            count += 1
            result = google_index()
            break
        except:
            print 'error'
            if count >= 3:
                break
            time.sleep(5)
    data = json.loads(result)
    for item in data:
        GoogleIndex.objects.update_or_create(date=item['date'], key=item['key'], defaults=item)
    return 'Finished.'

#淘宝销量 对应model： CompetitorSales, TaobaoDetail
@shared_task
def get_taobao_sales():
    result = '[]'
    count = 0
    while True:
        try:
            count += 1
            crawler = TaobaoCrawler()
            result = crawler.main()
            break
        except:
            print 'error'
            if count >= 3:
                break
            time.sleep(5)
    data = json.loads(result, encoding="utf-8")
    for item in data:
        date = item['date']
        # temp = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        # yesterday = (temp - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        commodity = item['commodity']
        taobao_total_sales = item['taobao_total_sales']
        stores = item['stores']
        old = CompetitorSales.objects.filter(date__lt=date, commodity=commodity).order_by('-date').first()
        if (old != None):
            if taobao_total_sales < old.taobao_total_sales * 0.7:
                taobao_sales = taobao_total_sales
            elif taobao_total_sales >= old.taobao_total_sales:
                taobao_sales = taobao_total_sales - old.taobao_total_sales
            else:
                taobao_sales = 0
        else:
            taobao_sales = taobao_total_sales
        temp = {'commodity': commodity, 'taobao_total_sales': taobao_total_sales, 'taobao_sales': taobao_sales, 'date': date}
        CompetitorSales.objects.update_or_create(date=item['date'], commodity=item['commodity'], defaults=temp)
        for store in stores:
            print store
            TaobaoDetail.objects.update_or_create(date=store['date'], store_id=store['store_id'], defaults=store)
    return 'Finished.'

#京东评论数 对应model： CompetitorSales
@shared_task
def get_jd_sales():
    result = '[]'
    count = 0
    while True:
        try:
            count += 1
            crawler = JDCrawler()
            result = crawler.main()
            break
        except:
            print 'error'
            if count >= 3:
                break
            time.sleep(5)
    data = json.loads(result)
    for item in data:
        date = item['date']
        commodity = item['commodity']
        old = CompetitorSales.objects.filter(date__lt=date, commodity=commodity).order_by('-date').first()
        if (old != None):
            if item['jd_total_sales'] < old.jd_total_sales * 0.7:
                item['jd_sales'] = item['jd_total_sales']
            elif item['jd_total_sales'] >= old.taobao_total_sales:
                item['jd_sales'] = item['jd_total_sales'] - old.jd_total_sales
            else:
                item['jd_sales'] = 0
        else:
            item['jd_sales'] = item['jd_total_sales']
        CompetitorSales.objects.update_or_create(date=item['date'], commodity=item['commodity'], defaults=item)
    return 'Finished.'

#亚马逊评论数 对应model： GlobalElectronicSales
@shared_task
def get_amazon_sales():
    result = '[]'
    count = 0
    while True:
        try:
            count += 1
            result = amanzon_crawler()
            break
        except:
            print 'error'
            if count >= 3:
                break
            time.sleep(5)
    data = json.loads(result, encoding="utf-8")
    for item in data:
        GlobalElectronicSales.objects.update_or_create(date=item['date'],country=item['country'], commodity=item['commodity'], site=item['site'], defaults=item)
    return 'Finished.'

#app错误情况 对应model： ErrorCondition
@shared_task
def get_error():
    today = datetime.datetime.today()
    end_date = today.strftime('%Y-%m-%d')
    start_date = (today - datetime.timedelta(days=6)).strftime('%Y-%m-%d')
    result = '[]'
    count = 0
    while True:
        try:
            count += 1
            crawler = UmengCrawler()
            result = crawler.getTotalError(start_date, end_date)
            break
        except:
            print 'error'
            if count >= 3:
                break
            time.sleep(5)
    data = json.loads(result)
    for item in data:
        ErrorCondition.objects.update_or_create(date=item['date'], product=item['product'], defaults=item)

    result = '[]'
    count = 0
    while True:
        try:
            count += 1
            crawler = UmengCrawler()
            result = crawler.getErrorRate(start_date, end_date)
            break
        except:
            print 'error'
            if count >= 3:
                break
            time.sleep(5)
    data = json.loads(result)
    for item in data:
        ErrorCondition.objects.update_or_create(date=item['date'], product=item['product'], defaults=item)
    return 'Finished.'

#app分享渠道 对应model： ShareChannel
@shared_task
def get_share_channel():
    today = datetime.datetime.today()
    end_date = today.strftime('%Y-%m-%d')
    start_date = (today - datetime.timedelta(days=5)).strftime('%Y-%m-%d')
    result = '[]'
    count = 0
    while True:
        try:
            count += 1
            crawler = UmengCrawler()
            result = crawler.getShareChannel(start_date, end_date)
            break
        except:
            print 'error'
            if count >= 3:
                break
            time.sleep(5)
    data = json.loads(result)
    for item in data:
        event_group_id = item['event_group_id']
        type = item['type']
        version = item['version']
        channel = item['channel']
        detail = item['data']
        product = item['product']

        for i in detail:
            try:
                device = int(i['device'])
            except:
                device = 0
            temp = {
                'channel': channel,
                'type': type,
                'count': i['count'],
                'device': device,
                'count_per_launch': i['count_per_launch']
            }
            ShareChannel.objects.update_or_create(date=i['date'],
                                                  product=product,
                                                  event_group_id=event_group_id,
                                                  version=version,
                                                  defaults=temp)
    return 'Finished.'

#app分享模式 对应model： ShareMode
@shared_task
def get_share_mode():
    today = datetime.datetime.today()
    end_date = today.strftime('%Y-%m-%d')
    start_date = (today - datetime.timedelta(days=5)).strftime('%Y-%m-%d')
    result = '[]'
    count = 0
    while True:
        try:
            count += 1
            crawler = UmengCrawler()
            result = crawler.getShareMode(start_date, end_date)
            break
        except:
            print 'error'
            if count >= 3:
                break
            time.sleep(5)
    data = json.loads(result)
    for item in data:
        event_group_id = item['event_group_id']
        mode = item['mode']
        version = item['version']
        detail = item['data']
        product = item['product']
        for i in detail:
            try:
                device = int(i['device'])
            except:
                device = 0
            temp = {
                'mode': mode,
                'count': i['count'],
                'device': device,
                'count_per_launch': i['count_per_launch']
            }
            ShareMode.objects.update_or_create(date=i['date'],
                                               product=product,
                                               event_group_id=event_group_id,
                                               version=version,
                                               defaults=temp)
    return 'Finished.'

#app分享数量和转化率 对应model： ShareCount
@shared_task
def get_share_count():
    today = datetime.datetime.today()
    end_date = today.strftime('%Y-%m-%d')
    start_date = (today - datetime.timedelta(days=4)).strftime('%Y-%m-%d')
    result = '[]'
    count = 0
    while True:
        try:
            count += 1
            crawler = UmengCrawler()
            result = crawler.getShareCount(start_date, end_date)
            break
        except:
            print 'error'
            if count >= 3:
                break
            time.sleep(5)
    data = json.loads(result)
    for item in data:
        type = item['type']
        version = item['version']
        flag = item['flag']
        detail = item['data']
        product = item['product']
        if flag == 'success':
            for i in detail:
                try:
                    device = int(i['device'])
                except:
                    device = 0
                temp = {
                    'success_count': i['count'],
                    'success_device': device,
                    'success_count_per_launch': i['count_per_launch']
                }
                ShareCount.objects.update_or_create(date=i['date'],
                                                      version=version,
                                                      product=product,
                                                      type=type,
                                                      defaults=temp)
        else:
            for i in detail:
                try:
                    device = int(i['device'])
                except:
                    device = 0
                temp = {
                    'try_count': i['count'],
                    'try_device': device,
                    'try_count_per_launch': i['count_per_launch']
                }
                ShareCount.objects.update_or_create(date=i['date'],
                                                      version=version,
                                                      product=product,
                                                      type=type,
                                                      defaults=temp)
    return 'Finished.'

#app视频图片拍摄数量 对应model： TakeCount
@shared_task
def get_take_count():
    today = datetime.datetime.today()
    end_date = today.strftime('%Y-%m-%d')
    start_date = (today - datetime.timedelta(days=5)).strftime('%Y-%m-%d')
    result = '[]'
    count = 0
    while True:
        try:
            count += 1
            crawler = UmengCrawler()
            result = crawler.getTakeCount(start_date, end_date)
            break
        except:
            print 'error'
            if count >= 3:
                break
            time.sleep(5)
    data = json.loads(result)
    for item in data:
        type = item['type']
        version = item['version']
        detail = item['data']
        product = item['product']
        if type == 'img':
            for i in detail:
                try:
                    device = int(i['device'])
                except:
                    device = 0
                temp = {
                    'img_count': i['count'],
                    'img_device': device,
                    'img_count_per_launch': i['count_per_launch']
                }
                TakeCount.objects.update_or_create(date=i['date'],product=product,
                                                      version=version,
                                                      defaults=temp)
        else:
            for i in detail:
                try:
                    device = int(i['device'])
                except:
                    device = 0
                temp = {
                    'video_count': i['count'],
                    'video_device': device,
                    'video_count_per_launch': i['count_per_launch']
                }
                TakeCount.objects.update_or_create(date=i['date'],product=product,
                                                      version=version,
                                                      defaults=temp)
    return 'Finished.'

#app用户分布 对应model： UserDistribution ， 其中港澳台算国外，中国减掉港澳台的数据
@shared_task
def get_user_distribution():
    delta = 4
    today = datetime.datetime.today()
    end_date = today.strftime('%Y-%m-%d')
    start_date = (today - datetime.timedelta(days=delta)).strftime('%Y-%m-%d')
    result = '[]'
    count = 0
    while True:
        try:
            count += 1
            crawler = UmengCrawler()
            result = crawler.getUserDistribution(start_date, end_date)
            break
        except:
            print 'error'
            if count >= 3:
                break
            time.sleep(5)
    data = json.loads(result)
    for item in data:
        if (item['location'] == '内蒙'):
            item['location'] = '内蒙古'
        UserDistribution.objects.update_or_create(date=item['date'], location=item['location'], product=item['product'], is_native=item['is_native'], defaults=item)

    for product in ['nano', 'air']:
        locations = [
                '香港',
                '澳门',
                '台湾'
            ]
        start = (today - datetime.timedelta(days=delta))
        end = (today + datetime.timedelta(days=1))
        result = UserDistribution.objects.filter(
            location__in=locations,
            product=product,
            date__range=(start, end)
        ).values(
                'date'
            ).annotate(
            launch_data_total=Sum('launch_data'),
            active_user_total=Sum('active_user'),
            new_user_total=Sum('new_user'),
        )
        for i in result:
            date = i['date']
            new_user_total = i['new_user_total']
            launch_data_total = i['launch_data_total']
            active_user_total = i['active_user_total']
            try:
                china = UserDistribution.objects.get(date=date, product=product, location='中国')
                china.new_user = china.new_user - new_user_total
                china.launch_data = china.launch_data - launch_data_total
                china.active_user = china.active_user - active_user_total
                china.save()
            except:
                pass

    return 'Finished.'

#新媒体粉丝数 对应model： MediaFan     （需要翻墙）
@shared_task
def get_fans():
    result = '[]'
    count = 0
    while True:
        try:
            count += 1
            result = fans_crawler()
            break
        except:
            print 'error'
            if count >= 3:
                break
            time.sleep(5)
    items = json.loads(result)
    for item in items:
        date = item['date']
        platform = item['platform']
        old = MediaFan.objects.filter(date__lt=date, platform=platform).order_by('-date').first()
        if (old != None):
          item['fans_increment'] = item['fans'] - old.fans
        else:
            item['fans_increment'] = 0
        MediaFan.objects.update_or_create(date=item['date'], platform=item['platform'], defaults=item)
    return 'Finished.'

#新媒体互动数（热度） 对应model： MediaData  （需要翻墙）
@shared_task
def get_media_data():
    result = '[]'
    count = 0
    while True:
        try:
            count += 1
            result = media_crawler()
            break
        except:
            print 'error'
            if count >= 3:
                break
            time.sleep(5)
    items = json.loads(result)
    for item in items:
        date = item['date']
        platform = item['platform']
        MediaData.objects.update_or_create(date=date, platform=platform, defaults=item)
    return 'Finished.'

#新媒体粉丝数 对应model： MediaFan     （需要翻墙）
@shared_task
def get_media_tag():
    result = '[]'
    count = 0
    while True:
        try:
            count += 1
            result = tag_crawler()
            break
        except:
            print 'error'
            if count >= 3:
                break
            time.sleep(5)
    items = json.loads(result)
    for item in items:
        if item['platform'] == 'twitter' or item['platform'] == 'youku' or item['platform'] == 'youtube' or item['platform'] == 'facebook':
            today = datetime.datetime.strptime(item['date'], "%Y-%m-%d")
            oneday = datetime.timedelta(days=1)
            yesterday = (today - oneday).strftime('%Y-%m-%d')
            try:
                old = MediaTag.objects.get(date=yesterday, platform=item['platform'], tag=item['tag'])
                new_count = old.count + item['count']
                item['count'] = new_count
            except:
                pass
        MediaTag.objects.update_or_create(date=item['date'], platform=item['platform'], tag=item['tag'],defaults=item)
    return 'Finished.'

#meltwater 对应model： Meltwater
@shared_task
def get_meltwater():
    today = datetime.datetime.today()
    end_date = today.strftime('%Y-%m-%d')
    start_date = (today - datetime.timedelta(days=6)).strftime('%Y-%m-%d')
    result = []
    count = 0
    while True:
        try:
            count += 1
            crawler = MeltwaterCrawler()
            result = crawler.main(start_date, end_date)
            break
        except:
            print 'error'
            if count >= 3:
                break
            time.sleep(5)
    data = result
    for item in data:
        Meltwater.objects.update_or_create(date=item['date'], key=item['key'], type=item['type'], country=item['country'], defaults=item)
    return 'Finished.'

#优酷视频统计 对应model： YoukuData
@shared_task
def get_youku():
    result = []
    count = 0
    while True:
        try:
            count += 1
            result = get_videos_info()
            break
        except:
            print 'error'
            if count >= 3:
                break
            time.sleep(5)
    data = result
    for item in data:
        YoukuData.objects.update_or_create(video_id=item['video_id'], date=item['date'], defaults=item)
    return 'Finished.'

#调用销售支持系统的一个接口，用于每天刷新数据库中卖出去的nano的激活状态
@shared_task
def refresh_active():
    request = urllib2.Request(url='http://sales.internal.insta360.com/sales/util/refresh_active')
    response = urllib2.urlopen(request)
    result = response.read()
    return result

#更新bi系统中insta_admin账号的密码，并发送邮件给指定的人
@shared_task
def update_password():
    password = password_updater()
    return password

import random
@shared_task
def fill_fans_data(start_date, end_date):
    start = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
    end = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
    platformsQuery = MediaFan.objects.filter(date__range=(start_date, end_date)).values('platform').distinct()
    platforms = []
    for item in platformsQuery:
        platforms.append(item['platform'])
    for platform in platforms:
        start_item = MediaFan.objects.get(platform=platform,date=start_date)
        end_item = MediaFan.objects.get(platform=platform, date=end_date)
        increment = end_item.fans - start_item.fans
        delta = (end - start).days
        avg = int(increment / delta)
        deviation = abs(int(avg * 0.3))
        fans = start_item.fans
        for i in range(1, delta):
            date = (start + datetime.timedelta(days=i)).strftime('%Y-%m-%d')
            fans += (avg + random.randint(- deviation, deviation))
            temp = {
                'fans': fans
            }
            MediaFan.objects.update_or_create(platform=platform,date=date,defaults=temp)
