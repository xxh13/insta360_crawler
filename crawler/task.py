#-*- coding: UTF-8 -*-
from __future__ import absolute_import
import os, commands, urllib2, json, datetime, time
from celery import task
from celery import shared_task
from celery.decorators import task
from celery.utils.log import get_task_logger
from .models import UseCondition
from .models import SearchIndex
from .models import CompetitorSales
from .models import UserDistribution
from .models import ErrorCondition
from .crawlers.umeng.UmengCrawler import UmengCrawler
from .crawlers.taobao.TaobaoCrawler import TaobaoCrawler
from .crawlers.jd.JDCrawler import JDCrawler
from .crawlers.baidu_index.main import *

logger = get_task_logger(__name__)


@shared_task
def test(a, b):
    return a+b


@shared_task
def get_use_condition():
    today = datetime.datetime.today()
    end_date = today.strftime('%Y-%m-%d')
    start_date = (today - datetime.timedelta(days=6)).strftime('%Y-%m-%d')
    result = ''
    while True:
        try:
            crawler = UmengCrawler()
            result = crawler.getUseCondition(start_date, end_date)
            break
        except:
            print 'error'
            time.sleep(5)
    data = json.loads(result)
    for item in data:
        UseCondition.objects.update_or_create(date=item['date'], defaults = item)
    return 'Finished.'


@shared_task
def get_baidu_index():
    today = datetime.datetime.today()
    end_date = today.strftime('%Y-%m-%d')
    start_date = (today - datetime.timedelta(days=6)).strftime('%Y-%m-%d')
    result = ''
    while True:
        try:
            result = baidu_index(start_date, end_date)
            break
        except:
            print 'error'
            time.sleep(5)
    data = json.loads(result)
    for item in data:
        SearchIndex.objects.update_or_create(date=item['date'], key=item['key'], defaults = item)
    return 'Finished.'


@shared_task
def get_taobao_sales():
    result = ''
    while True:
        try:
            crawler = TaobaoCrawler()
            result = crawler.main()
            break
        except:
            print 'error'
            time.sleep(5)
    data = json.loads(result)
    for item in data:
        date = item['date']
        # temp = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        # yesterday = (temp - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        commodity = item['commodity']
        old = CompetitorSales.objects.filter(date__lt=date, commodity=commodity).order_by('-date').first()
        if (old != None):
            if item['taobao_total_sales'] < old.taobao_total_sales * 0.7:
                item['taobao_sales'] = item['taobao_total_sales']
            elif item['taobao_total_sales'] >= old.taobao_total_sales:
                item['taobao_sales'] = item['taobao_total_sales'] - old.taobao_total_sales
            else:
                item['taobao_sales'] = 0
        else:
            item['taobao_sales'] = item['taobao_total_sales']
        CompetitorSales.objects.update_or_create(date=item['date'], commodity=item['commodity'], defaults = item)
    return 'Finished.'


@shared_task
def get_jd_sales():
    result = ''
    while True:
        try:
            crawler = JDCrawler()
            result = crawler.main()
            break
        except:
            print 'error'
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
        CompetitorSales.objects.update_or_create(date=item['date'], commodity=item['commodity'], defaults = item)
    return 'Finished.'


@shared_task
def get_error():
    today = datetime.datetime.today()
    end_date = today.strftime('%Y-%m-%d')
    start_date = (today - datetime.timedelta(days=6)).strftime('%Y-%m-%d')
    result = ''
    while True:
        try:
            crawler = UmengCrawler()
            result = crawler.getTotalError(start_date, end_date)
            break
        except:
            print 'error'
            time.sleep(5)
    data = json.loads(result)
    for item in data:
        ErrorCondition.objects.update_or_create(date=item['date'], defaults = item)
    return 'Finished.'


@shared_task
def get_user_distribution():
    today = datetime.datetime.today()
    end_date = today.strftime('%Y-%m-%d')
    start_date = (today - datetime.timedelta(days=6)).strftime('%Y-%m-%d')
    result = ''
    while True:
        try:
            crawler = UmengCrawler()
            result = crawler.getUserDistribution(start_date, end_date)
            break
        except:
            print 'error'
            time.sleep(5)
    data = json.loads(result)
    for item in data:
        if (item['location'] == '内蒙'):
            item['location'] = '内蒙古'
        UserDistribution.objects.update_or_create(date=item['date'], location=item['location'], defaults = item)
    return 'Finished.'