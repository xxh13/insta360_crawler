# coding=utf-8

import json, sys, datetime, time

reload(sys)
sys.setdefaultencoding('utf-8')

from django.http import HttpResponse, JsonResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt
from models import SalesStatus
from models import ElectronicSales
from models import UserDistribution
from models import UseCondition
from models import SearchIndex
from task import get_user_distribution as t

@csrf_exempt
def sales_status(request):
    if request.method == 'POST':
        body = json.loads(request.body, encoding='utf-8')
        data = body['data']
        week = body['week']
        is_native = body['is_native']
        SalesStatus.objects.filter(week=week, is_native=is_native).delete()
        for item in data:
            SalesStatus.objects.update_or_create(week=item['week'], location=item['location'], defaults=item)
        return HttpResponse('Task submitted.')
    elif request.method == 'GET':
        para = request.GET
        today = datetime.datetime.today()
        delta = today.weekday()
        is_native = 1
        if para.__contains__('is_native'):
            is_native = para.__getitem__('is_native')
        week = (today - datetime.timedelta(days=delta)).strftime('%Y-%m-%d')
        if para.__contains__('week'):
            week = para.__getitem__('week')
        else:
            weeks = SalesStatus.objects.filter(is_native=is_native).order_by('-week')
            for item in weeks:
                 week = item.week
                 break
        data = []
        res = SalesStatus.objects.filter(week=week, is_native=is_native)
        for item in res:
            temp = {'week': item.week,'location': item.location,'pick_up': item.pick_up,'sales_online': item.sales_online,'sales_offline': item.sales_offline,'inventory_first': item.inventory_first,'inventory_lower': item.inventory_lower,'reject':item.reject,'is_native':item.is_native}
            data.append(temp)
        result = {'week': week, 'data':data }
        return JsonResponse(result,safe=False)
    else:
        return HttpResponse('Error.')

@csrf_exempt
def electronic_sales(request):
    if request.method == 'POST':
        body = json.loads(request.body, encoding='utf-8')
        data = body['data']
        week = body['week']
        ElectronicSales.objects.filter(week=week).delete()
        for item in data:
            ElectronicSales.objects.update_or_create(week=item['week'], location=item['location'], defaults=item)
        return HttpResponse('Task submitted.')
    elif request.method == 'GET':
        para = request.GET
        today = datetime.datetime.today()
        delta = today.weekday()
        week = (today - datetime.timedelta(days=delta)).strftime('%Y-%m-%d')
        if para.__contains__('week'):
            week = para.__getitem__('week')
        else:
            weeks = ElectronicSales.objects.dates('week', 'day', order='DESC')
            for item in weeks:
                week = item
                break
        data = []
        res = ElectronicSales.objects.filter(week=week)
        for item in res:
            temp = {'week': item.week,'location': item.location,'view': item.view,'visitor': item.visitor,'payment': item.payment,'number': item.number,'buyer':item.buyer}
            data.append(temp)
        result = {'week': week, 'data':data }
        return JsonResponse(result,safe=False)
    else:
        return HttpResponse('Error.')

@csrf_exempt
def user_distribution(request):
    if request.method == 'POST':
        return HttpResponse('Task submitted.')
    elif request.method == 'GET':
        para = request.GET
        today = datetime.datetime.today()
        start_time = (today - datetime.timedelta(days=7)).strftime('%Y-%m-%d')
        end_time = (today + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        if para.__contains__('start_time'):
            start_time = para.__getitem__('start_time')
        if para.__contains__('end_time'):
            end_time = para.__getitem__('end_time')
        result = []
        res = UserDistribution.objects.filter(date__range=(start_time, end_time))
        for item in res:
            temp = {'date': item.date,'location': item.location,'active_user': item.active_user,'is_native': item.is_native}
            result.append(temp)
        return JsonResponse(result,safe=False)
    else:
        return HttpResponse('Error.')

@csrf_exempt
def use_condition(request):
    if request.method == 'POST':
        return HttpResponse('Task submitted.')
    elif request.method == 'GET':
        para = request.GET
        today = datetime.datetime.today()
        start_time = (today - datetime.timedelta(days=7)).strftime('%Y-%m-%d')
        end_time = (today + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        if para.__contains__('start_time'):
            start_time = para.__getitem__('start_time')
        if para.__contains__('end_time'):
            end_time = para.__getitem__('end_time')
        result = []
        res = UseCondition.objects.filter(date__range=(start_time, end_time))
        for item in res:
            temp = {'date': item.date,'new_user': item.new_user,'active_user': item.active_user,'duration': item.duration}
            result.append(temp)
        return JsonResponse(result,safe=False)
    else:
        return HttpResponse('Error.')

@csrf_exempt
def search_index(request):
    if request.method == 'POST':
        return HttpResponse('Task submitted.')
    elif request.method == 'GET':
        para = request.GET
        today = datetime.datetime.today()
        start_time = (today - datetime.timedelta(days=7)).strftime('%Y-%m-%d')
        end_time = (today + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        if para.__contains__('start_time'):
            start_time = para.__getitem__('start_time')
        if para.__contains__('end_time'):
            end_time = para.__getitem__('end_time')
        result = []
        res = SearchIndex.objects.filter(date__range=(start_time, end_time))
        for item in res:
            temp = {'date': item.date,'key': item.key,'baidu_index': item.baidu_index}
            result.append(temp)
        return JsonResponse(result,safe=False)
    else:
        return HttpResponse('Error.')

@csrf_exempt
def error_condition(request):
    if request.method == 'POST':
        return HttpResponse('Task submitted.')
    elif request.method == 'GET':
        para = request.GET
        today = datetime.datetime.today()
        start_time = (today - datetime.timedelta(days=7)).strftime('%Y-%m-%d')
        end_time = (today + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        if para.__contains__('start_time'):
            start_time = para.__getitem__('start_time')
        if para.__contains__('end_time'):
            end_time = para.__getitem__('end_time')
        result = []
        res = SearchIndex.objects.filter(date__range=(start_time, end_time))
        for item in res:
            temp = {'date': item.date, 'total_error': item.total_error}
            result.append(temp)
        return JsonResponse(result, safe=False)
    else:
        return HttpResponse('Error.')

@csrf_exempt
def test(request):
    if request.method == 'POST':
        return HttpResponse('Task submitted.')
    elif request.method == 'GET':
        t('2016-06-10','2016-08-16')
        return HttpResponse('Task submitted.')
    else:
        return HttpResponse('Error.')