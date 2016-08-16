from __future__ import absolute_import
import os, commands, urllib2, json
from celery import task
from celery import shared_task
from celery.decorators import task
from celery.utils.log import get_task_logger
from .models import UseCondition
from .models import SearchIndex
from .models import CompetitorSales
from .models import UserDistribution
from .crawlers.umeng.UmengCrawler import UmengCrawler
from .crawlers.taobao.TaobaoCrawler import TaobaoCrawler
from .crawlers.baidu_index.main import *

logger = get_task_logger(__name__)


@shared_task
def test(a, b):
    return a+b

@shared_task
def get_use_condition(start_date, end_date):
    crawler = UmengCrawler()
    result = crawler.getUseCondition(start_date, end_date)
    data = json.loads(result)
    for item in data:
        UseCondition.objects.update_or_create(date=item['date'], defaults = item)
    return 'Finished.'

@shared_task
def get_baidu_index(start_date, end_date):
    result = baidu_index(start_date, end_date)
    data = json.loads(result)
    for item in data:
        SearchIndex.objects.update_or_create(date=item['date'], key=item['key'], defaults = item)
    return 'Finished.'

@shared_task
def get_taobao_sales(start_date, end_date):
    crawler = TaobaoCrawler()
    result = crawler.main()
    data = json.loads(result)
    for item in data:
        CompetitorSales.objects.update_or_create(date=item['date'], commodity=item['commodity'], defaults = item)
    return 'Finished.'

@shared_task
def get_user_distribution(start_date, end_date):
    crawler = UmengCrawler()
    result = crawler.getUserDistribution(start_date, end_date)
    data = json.loads(result)
    for item in data:
        UserDistribution.objects.update_or_create(date=item['date'], location=item['location'], defaults = item)
    return 'Finished.'