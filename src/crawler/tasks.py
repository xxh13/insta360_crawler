# -*- coding: UTF-8 -*-
'''
get_google_index()
get_fans()
get_media_data()
需要翻墙

get_amazon_sales()
get_taobao_sales()
get_jd_sales()
不是很稳定
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
from .models import ShareCount
from .models import TakeCount
from .models import MediaFan
from .models import MediaData
from .models import TaobaoDetail
from .models import GlobalElectronicSales
from .crawlers.umeng.UmengCrawler import UmengCrawler
from .crawlers.taobao.TaobaoCrawler import TaobaoCrawler
from .crawlers.jd.JDCrawler import JDCrawler
from .crawlers.baidu_index.main import *
from .crawlers.amazon.amazon_crawler import main as amanzon_crawler
from .crawlers.google_index.google_trends import google_index
from .crawlers.fans_crawler.main import main as fans_crawler
from .crawlers.media_crawler.main import main as media_crawler
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
        UseCondition.objects.update_or_create(date=item['date'], defaults=item)
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
        # temp = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        # yesterday = (temp - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
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
        ErrorCondition.objects.update_or_create(date=item['date'], defaults=item)

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
        ErrorCondition.objects.update_or_create(date=item['date'], defaults=item)
    return 'Finished.'

#app分享渠道 对应model： ShareChannel
@shared_task
def get_share_channel():
    today = datetime.datetime.today()
    end_date = today.strftime('%Y-%m-%d')
    start_date = (today - datetime.timedelta(days=2)).strftime('%Y-%m-%d')
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
                                                  event_group_id=event_group_id,
                                                  version=version,
                                                  defaults=temp)
    return 'Finished.'

#app分享数量和转化率 对应model： ShareCount
@shared_task
def get_share_count():
    today = datetime.datetime.today()
    end_date = today.strftime('%Y-%m-%d')
    start_date = (today - datetime.timedelta(days=2)).strftime('%Y-%m-%d')
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
                                                      type=type,
                                                      defaults=temp)
    return 'Finished.'

#app视频图片拍摄数量 对应model： TakeCount
@shared_task
def get_take_count():
    today = datetime.datetime.today()
    end_date = today.strftime('%Y-%m-%d')
    start_date = (today - datetime.timedelta(days=2)).strftime('%Y-%m-%d')
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
                TakeCount.objects.update_or_create(date=i['date'],
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
                TakeCount.objects.update_or_create(date=i['date'],
                                                      version=version,
                                                      defaults=temp)
    return 'Finished.'

#app用户分布 对应model： UserDistribution ， 其中港澳台算国外，中国减掉港澳台的数据
@shared_task
def get_user_distribution():
    delta = 2
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
        UserDistribution.objects.update_or_create(date=item['date'], location=item['location'], is_native=item['is_native'], defaults=item)

    locations = [
            '香港',
            '澳门',
            '台湾'
        ]
    start = (today - datetime.timedelta(days=delta))
    end = (today + datetime.timedelta(days=1))
    result = UserDistribution.objects.filter(
        location__in=locations,
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
            china = UserDistribution.objects.get(date=date, location='中国')
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
