# -*- coding: UTF-8 -*-
from __future__ import absolute_import
from celery import shared_task
from celery.utils.log import get_task_logger
from django.contrib.auth.models import User
from .models import UseCondition
from .models import SearchIndex
from .models import GoogleIndex
from .models import CompetitorSales
from .models import UserDistribution
from .models import ErrorCondition
from .models import ShareChannel
from .models import ShareCount
from .models import MediaFan
from .models import TaobaoDetail
from .crawlers.umeng.UmengCrawler import UmengCrawler
from .crawlers.taobao.TaobaoCrawler import TaobaoCrawler
from .crawlers.jd.JDCrawler import JDCrawler
from .crawlers.baidu_index.main import *
from .crawlers.google_index.google_trends import google_index
from .crawlers.fans_crawler.main import main as fans_crawler
from .util.admin import password_updater

import datetime
import time
import urllib2


logger = get_task_logger(__name__)


@shared_task
def test(a, b):
    print a + b
    return a + b


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
        # print stores
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


@shared_task
def get_user_distribution():
    today = datetime.datetime.today()
    end_date = today.strftime('%Y-%m-%d')
    start_date = (today - datetime.timedelta(days=2)).strftime('%Y-%m-%d')
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
        UserDistribution.objects.update_or_create(date=item['date'], location=item['location'], defaults=item)
    return 'Finished.'


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


@shared_task
def refresh_active():
    request = urllib2.Request(url='http://sales.internal.insta360.com/sales/util/refresh_active')
    response = urllib2.urlopen(request)
    result = response.read()
    return result


@shared_task
def update_password():
    password = password_updater()
    return password
