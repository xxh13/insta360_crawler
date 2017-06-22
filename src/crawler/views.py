# coding=utf-8

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
from django.forms.models import model_to_dict
from models import SalesStatus
from models import ElectronicSales
from models import UserDistribution
from models import UseCondition
from models import ErrorCondition
from models import SearchIndex
from models import GoogleIndex
from models import CompetitorSales
from models import GlobalElectronicSales
from models import ShareChannel
from models import ShareMode
from models import ShareCount
from models import TakeCount
from models import MediaFan
from models import MediaData
from models import MediaTag
from models import Meltwater
from models import Log
from models import TaobaoDetail
from tasks import *
from tasks import get_fans as f
from tasks import get_google_index as g
from util.dict import media_dict
from view.views_admin import *
from view.views_video import *

import json
import sys
import datetime
import urllib
import collections

reload(sys)
sys.setdefaultencoding('utf-8')

#销售录入系统的增删该查接口
@csrf_exempt
def sales_status(request):
    if request.method == 'POST':
        body = json.loads(request.body, encoding='utf-8')
        data = body['data']
        week = body['week']
        product = body['product']
        username = body['username']
        table = '国内销售'
        is_native = body['is_native']
        if is_native == 0:
            table = '海外销售'

        week_date = datetime.datetime.strptime(week, '%Y-%m-%d').date()
        next_week = (week_date + datetime.timedelta(days=7)).strftime('%Y-%m-%d')
        old = SalesStatus.objects.filter(week=week, is_native=is_native, product=product).values('location')
        s = set()
        for item in old:
            s.add(item['location'])

        for item in data:

            result = SalesStatus.objects.update_or_create(
                week=item['week'],
                location=item['location'],
                product=item['product'],
                is_native=is_native,
                defaults=item
            )

            if result[1]:
                operator = 'add'
            else:
                operator = 'update'

            Log.objects.create(
                username=username,
                week=item['week'],
                table=table,
                location=item['location'],
                operator=operator
            )
            temp = {
                'week': next_week,
                'location': item['location'],
                'is_native': is_native,
                'agent_name': item['agent_name'],
                'agent_type': item['agent_type'],
                'agent_price': item['agent_price']
            }
            SalesStatus.objects.update_or_create(
                week=next_week,
                location=item['location'],
                product=item['product'],
                is_native=is_native,
                defaults = temp
            )

            if item['location'] in s:
                s.remove(item['location'])

        for i in s:
            SalesStatus.objects.filter(
                week=week,
                is_native=is_native,
                location=i,
                product=product
            ).delete()

            Log.objects.create(
                username=username,
                week=week,
                table=table,
                location=i,
                operator='delete'
            )

        return HttpResponse('Task submitted.')

    elif request.method == 'GET':

        para = request.GET
        today = datetime.datetime.today()
        delta = today.weekday()
        product = para.get('product', 'nano')
        is_native = para.get('is_native', 1)
        week = (today - datetime.timedelta(days=delta)).strftime('%Y-%m-%d')
        if para.__contains__('week'):
            week = para.__getitem__('week')
        else:
            weeks = SalesStatus.objects.filter(is_native=is_native, product=product).order_by('-week')
            for item in weeks:
                week = (item.week - datetime.timedelta(days=7)).strftime('%Y-%m-%d')
                break

        data = []
        res = SalesStatus.objects.filter(week=week, is_native=is_native, product=product)

        for item in res:
            temp = {
                'week': item.week,
                'product': item.product,
                'location': item.location,
                'pick_up': item.pick_up,

                'agent_name': item.agent_name,
                'agent_type': item.agent_type,
                'agent_price': item.agent_price,

                'sales_online': item.sales_online,
                'sales_offline': item.sales_offline,
                'sales_offline_count': item.sales_offline_count,
                'inventory_first': item.inventory_first,
                'inventory_lower': item.inventory_lower,
                'reject': item.reject,
                'is_native': item.is_native
            }

            data.append(temp)
        result = {
            'week': week,
            'data': data
        }
        return JsonResponse(result, safe=False)
    else:
        return HttpResponse('Error.')

#bi系统->Nano 零售渠道->国内、海外销售情况
@csrf_exempt
def get_sales_status(request):
    if request.method == 'POST':
        return HttpResponse('Do Nothing.')
    elif request.method == 'GET':
        para = request.GET
        today = datetime.datetime.today()
        start_time = (today - datetime.timedelta(days=29)).strftime('%Y-%m-%d')
        end_time = (today + datetime.timedelta(days=1)).strftime('%Y-%m-%d')

        product = para.get('product', 'nano')
        is_native = para.get('is_native', 1)
        end_time = para.get('end_time', end_time)
        location = para.get('location', 'all')
        if para.__contains__('start_time'):
            startTime = datetime.datetime.strptime(para.__getitem__('start_time'), '%Y-%m-%d').date()
            start_time = (startTime - datetime.timedelta(days=6)).strftime('%Y-%m-%d')

        data = []
        index = []
        if location == 'all':
            res = SalesStatus.objects.filter(
                week__range=(start_time, end_time),
                is_native=is_native,
                product=product
            ).values(
                'week'
            ).annotate(
                pick_up_total=Sum('pick_up'),
                sales_online_total=Sum('sales_online'),
                sales_offline_total=Sum('sales_offline'),
                sales_offline_count_total=Sum('sales_offline_count'),
                inventory_first_total=Sum('inventory_first'),
                inventory_lower_total=Sum('inventory_lower'),
                reject_total=Sum('reject')
            ).order_by('week')

            for item in res:
                temp = {
                    'pick_up': item['pick_up_total'],
                    'sales_online': item['sales_online_total'],
                    'sales_offline': item['sales_offline_total'],
                    'sales_offline_count': item['sales_offline_count_total'],
                    'inventory_first': item['inventory_first_total'],
                    'inventory_lower': item['inventory_lower_total'],
                    'reject': item['reject_total']
                }
                end = (item['week'] + datetime.timedelta(days=6)).strftime('%m-%d')
                index.append(item['week'].strftime('%m-%d') + '~' + end)
                data.append(temp)

            last_res = SalesStatus.objects.filter(
                week__lt=start_time,
                is_native=is_native,
                product=product
            ).values(
                'week'
            ).annotate(
                last_inventory_first=Sum('inventory_first'),
                last_inventory_lower=Sum('inventory_lower'),
                last_reject=Sum('reject'),
            ).order_by('-week')


            last_inventory_first = 0
            last_inventory_lower = 0
            last_reject = 0

            for item in last_res:
                last_inventory_first = item['last_inventory_first']
                last_inventory_lower = item['last_inventory_lower']
                last_reject = item['last_reject']
                break

            res_last = {}
            res_last['inventory_first'] = last_inventory_first
            res_last['inventory_lower'] = last_inventory_lower
            res_last['reject'] = last_reject


        else:
            res = SalesStatus.objects.filter(
                week__range=(start_time, end_time),
                is_native=is_native,
                product=product,
                location=location).order_by('week')
            for item in res:
                temp = {
                    'pick_up': item.pick_up,
                    'sales_online': item.sales_online,
                    'sales_offline': item.sales_offline,
                    'sales_offline_count': item.sales_offline_count,
                    'inventory_first': item.inventory_first,
                    'inventory_lower': item.inventory_lower,
                    'reject': item.reject
                }

                end = (item.week + datetime.timedelta(days=6)).strftime('%m-%d')
                index.append(item.week.strftime('%m-%d') + '~' + end)
                data.append(temp)

            last = SalesStatus.objects.filter(week__lt=start_time,
                                              is_native=is_native,
                                              location=location,
                                              product=product
                                              ).order_by('-week').first()
            last_inventory_first = 0
            last_inventory_lower = 0
            last_reject = 0

            if (last != None):
                last_inventory_first = last.inventory_first
                last_inventory_lower = last.inventory_lower
                last_reject = last.reject
            res_last = {}
            res_last['inventory_first'] = last_inventory_first
            res_last['inventory_lower'] = last_inventory_lower
            res_last['reject'] = last_reject

        locations = SalesStatus.objects.filter(is_native=is_native, product=product).values('location').distinct()
        temp = []
        for item in locations:
            res_temp = SalesStatus.objects.filter(is_native=is_native, product=product, location=item['location']).order_by('-week').first()
            location_agent = {
                'location': item['location'],
                'agent_name': res_temp.agent_name,
                'agent_type': res_temp.agent_type,
                'agent_price': res_temp.agent_price
            }
            temp.append(location_agent)
        result = {
            'locations': temp,
            'data': data,
            'last': res_last,
            'index': index
        }
        return JsonResponse(result, safe=False)
    else:
        return HttpResponse('Error.')

# 销售录入系统电商销售的增删该查接口
@csrf_exempt
def electronic_sales(request):
    if request.method == 'POST':
        body = json.loads(request.body, encoding='utf-8')
        data = body['data']
        week = body['week']
        product = body['product']
        username = body['username']
        table = '电商销售'
        week_date = datetime.datetime.strptime(week, '%Y-%m-%d').date()
        next_week = (week_date + datetime.timedelta(days=7)).strftime('%Y-%m-%d')
        old = ElectronicSales.objects.filter(week=week, product=product).values('location')
        s = set()
        for item in old:
            s.add(item['location'])
        for item in data:
            result = ElectronicSales.objects.update_or_create(
                week=item['week'],
                product=item['product'],
                location=item['location'],
                defaults=item
            )
            if result[1]:
                operator = 'add'
            else:
                operator = 'update'
            Log.objects.create(
                username=username,
                week=item['week'],
                table=table,
                location=item['location'],
                operator=operator
            )
            ElectronicSales.objects.update_or_create(
                week=next_week,
                product=product,
                location=item['location']
            )
            if item['location'] in s:
                s.remove(item['location'])
        for i in s:
            ElectronicSales.objects.filter(week=week, location=i, product=product).delete()
            Log.objects.create(username=username, week=week, table=table, location=i, operator='delete')
        return HttpResponse('Task submitted.')
    elif request.method == 'GET':
        para = request.GET
        product = para.get('product', 'nano')
        today = datetime.datetime.today()
        delta = today.weekday()
        week = (today - datetime.timedelta(days=delta)).strftime('%Y-%m-%d')
        if para.__contains__('week'):
            week = para.__getitem__('week')
        else:
            weeks = ElectronicSales.objects.filter(product=product).dates('week', 'day', order='DESC')
            for item in weeks:
                week = (item - datetime.timedelta(days=7)).strftime('%Y-%m-%d')
                break
        data = []
        res = ElectronicSales.objects.filter(week=week, product=product)
        for item in res:
            temp = {
                'week': item.week,
                'location': item.location,
                'product': item.product,
                'view': item.view,
                'visitor': item.visitor,
                'payment': item.payment,
                'number': item.number,
                'buyer': item.buyer
            }
            data.append(temp)
        result = {'week': week, 'data': data}
        return JsonResponse(result, safe=False)
    else:
        return HttpResponse('Error.')

#bi系统->Nano 零售渠道->自有电商渠道
@csrf_exempt
def get_electronic_sales(request):
    if request.method == 'POST':
        return HttpResponse('Do Nothing.')
    elif request.method == 'GET':
        para = request.GET
        today = datetime.datetime.today()
        start_time = (today - datetime.timedelta(days=29)).strftime('%Y-%m-%d')
        end_time = (today + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        product = para.get('product', 'nano')
        end_time = para.get('end_time', end_time)
        start_time = para.get('start_time', start_time)
        location = para.get('location', 'all')
        products = product.split(',')
        print products
        # if para.__contains__('start_time'):
        #     startTime = datetime.datetime.strptime(para.__getitem__('start_time'), '%Y-%m-%d').date()
        #     start_time = (startTime - datetime.timedelta(days=6)).strftime('%Y-%m-%d')
        data = []
        index = []
        if location == 'all':
            res = ElectronicSales.objects.filter(
                week__range=(start_time, end_time),
                product__in=products
            ).values('week').annotate(
                view_total=Sum('view'),
                visitor_total=Sum('visitor'),
                payment_total=Sum('payment'),
                number_total=Sum('number'),
                buyer_total=Sum('buyer')).order_by('week')
            for item in res:
                temp = {
                    'view': item['view_total'],
                    'visitor': item['visitor_total'],
                    'payment': item['payment_total'],
                    'number': item['number_total'],
                    'buyer': item['buyer_total']
                }
                # end = (item['week'] + datetime.timedelta(days=6)).strftime('%m-%d')
                # index.append(item['week'].strftime('%m-%d') + '~' + end)
                index.append(item['week'].strftime('%m-%d'))
                data.append(temp)
        else:
            res = ElectronicSales.objects.filter(
                week__range=(start_time, end_time),
                location=location,
                product__in=products
            ).order_by('week')
            for item in res:
                temp = {
                    'view': item.view,
                    'visitor': item.visitor,
                    'payment': item.payment,
                    'number': item.number,
                    'buyer': item.buyer
                }
                # end = (item.week + datetime.timedelta(days=6)).strftime('%m-%d')
                # index.append(item.week.strftime('%m-%d') + '~' + end)
                index.append(item.week.strftime('%m-%d'))
                data.append(temp)
        locations = list(ElectronicSales.objects.filter(product=product).values_list('location', flat=True).distinct())
        products = list(ElectronicSales.objects.values_list('product', flat=True).distinct())
        result = {
            'locations': locations,
            'products': products,
            'data': data,
            'index': index
        }
        return JsonResponse(result, safe=False)
    else:
        return HttpResponse('Error.')

#bi系统->Nano App使用情况->APP用户区域分布
@csrf_exempt
def user_distribution(request):
    if request.method == 'POST':
        return HttpResponse('Task submitted.')
    elif request.method == 'GET':
        para = request.GET
        today = datetime.datetime.today()
        start_time = (today - datetime.timedelta(days=6)).strftime('%Y-%m-%d')
        end_time = (today + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        start_time = para.get('start_time', start_time)
        end_time = para.get('end_time', end_time)
        product = para.get('product_type', 'nano')
        res_native = []
        res_abroad = []
        if product == 'all':
            native = UserDistribution.objects.filter(date__range=(start_time, end_time),
                                                     is_native=1).values(
                'location').annotate(total=Sum('new_user')).order_by('-total')
            abroad = UserDistribution.objects.filter(date__range=(start_time, end_time),
                                                     is_native=0).values(
                'location').annotate(total=Sum('new_user')).order_by('-total')
        else:
            native = UserDistribution.objects.filter(date__range=(start_time, end_time), product=product, is_native=1).values(
                'location').annotate(total=Sum('new_user')).order_by('-total')
            abroad = UserDistribution.objects.filter(date__range=(start_time, end_time), product=product, is_native=0).values(
                'location').annotate(total=Sum('new_user')).order_by('-total')
        fp = open('crawler/util/dict.json', 'r')
        dict = json.loads(fp.read(), encoding='utf-8')
        fp.close()
        for item in native:
            res_native.append(item)
        for item in abroad:
            try:
                location = dict[item['location']]
            except KeyError:
                location = item['location']
            item['location'] = location
            res_abroad.append(item)
        result = {'abroad': res_abroad, 'native': res_native}
        return JsonResponse(result, safe=False)
    else:
        return HttpResponse('Error.')

#bi系统->Nano App使用情况->APP用户区域分布->区域对比
@csrf_exempt
def user_area(request):
    if request.method == 'POST':
        return HttpResponse('Task submitted.')
    elif request.method == 'GET':
        para = request.GET
        today = datetime.datetime.today()
        start_time = (today - datetime.timedelta(days=29)).strftime('%Y-%m-%d')
        end_time = (today + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        start_time = para.get('start_time', start_time)
        end_time = para.get('end_time', end_time)
        product = para.get('product_type', 'nano')
        is_native = para.get('is_native', 1)

        if product == 'all':
            res = UserDistribution.objects.filter(date__range=(start_time, end_time),
                                                  is_native=is_native)
        else:
            res = UserDistribution.objects.filter(date__range=(start_time, end_time),
                                                  product=product,
                                                  is_native=is_native
                                                  )
        locations = res.values('location').annotate(total=Sum('new_user')).order_by('-total')[:10]
        location_list = []
        for location in locations:
            location_list.append(location['location'])
        dates = res.dates('date', 'day')
        data = []
        index = []
        for date in dates:
            index.append(date.strftime('%m-%d'))
            temp = collections.OrderedDict()
            query = res.filter(date=date, location__in=location_list).values(
                'location').annotate(new_user=Sum('new_user'))
            for item in query:
                temp[item['location']] = item['new_user']
            data.append(temp)
        result = {
            'data': data,
            'locations': location_list,
            'index': index
        }
        return JsonResponse(result, safe=False)
    else:
        return HttpResponse('Error.')

#bi系统->Nano App使用情况->用户概况
@csrf_exempt
def use_condition(request):
    if request.method == 'POST':
        return HttpResponse('Task submitted.')
    elif request.method == 'GET':
        para = request.GET
        today = datetime.datetime.today()
        start_time = (today - datetime.timedelta(days=6)).strftime('%Y-%m-%d')
        end_time = (today + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        start_time = para.get('start_time', start_time)
        end_time = para.get('end_time', end_time)
        product = para.get('product_type', 'nano')
        data = []
        if product == 'all':
            res = UseCondition.objects.filter(date__range=(start_time, end_time)).values(
                'date'
            ).annotate(
                new_user=Sum('new_user'),
                active_user=Sum('active_user'),
                duration = Sum('duration')
            ).order_by('date')
        else:
            res = UseCondition.objects.filter(date__range=(start_time, end_time), product=product).order_by('date').values()
        index = []
        for item in res:
            index.append(item['date'].strftime('%m-%d'))
            temp = {'date': item['date'].strftime('%m-%d'), 'new_user': item['new_user'], 'active_user': item['active_user'],
                        'duration': item['duration']}
            data.append(temp)
        result = {
            'data': data,
            'index': index
        }
        return JsonResponse(result, safe=False)
    else:
        return HttpResponse('Error.')

#bi系统->Nano内容分享->分享渠道占比
@csrf_exempt
def share_channel(request):
    if request.method == 'POST':
        return HttpResponse('Task submitted.')
    elif request.method == 'GET':
        para = request.GET
        today = datetime.datetime.today()
        start_time = (today - datetime.timedelta(days=6)).strftime('%Y-%m-%d')
        end_time = (today + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        start_time = para.get('start_time', start_time)
        end_time = para.get('end_time', end_time)
        product = para.get('product_type', 'nano')
        mode = para.get('mode', 'day')
        type = para.get('type', 'img')
        version = para.get('version', 'all')
        data = []
        versions = list(ShareChannel.objects.filter(product=product,type=type).order_by('-version').values_list('version', flat=True).distinct())
        if version == 'all':
            res = ShareChannel.objects.filter(
                date__range=(start_time, end_time),
                type=type,
                product=product
            ).values(
                'date', 'channel'
            ).annotate(
                count_total=Sum('count')
            ).order_by('date')
            dates = res.dates('date', 'day')
            items = list(ShareChannel.objects.filter(
                date__range=(start_time, end_time),
                type=type,
                product=product
            ).values_list('channel',flat=True).distinct())
            index = []
            for date in dates:
                index.append(date.strftime('%m-%d'))
                month_start = (date - datetime.timedelta(days=29)).strftime('%Y-%m-%d')
                res_temp = res.filter(date=date).order_by('count_total')
                temp = collections.OrderedDict()
                for item in res_temp:
                    item_temp = {
                        'today': item['count_total']
                    }
                    if mode == 'month':
                        month_res = ShareChannel.objects.filter(
                            date__range=(month_start, date.strftime('%Y-%m-%d')),
                            type=type,
                            product=product,
                            channel=item['channel']
                        ).values('channel').annotate(
                            count_total=Sum('count')
                        )
                        item_temp['month'] =  month_res[0]['count_total']
                    temp[item['channel']] = item_temp
                data.append(temp)
            result = {
                'versions': versions,
                'data': data,
                'index': index,
                'items': items,
                'mode': mode
            }
            return JsonResponse(result, safe=False)

        res = ShareChannel.objects.filter(date__range=(start_time, end_time), product=product, version=version,type=type).order_by('date')
        dates = res.dates('date', 'day')
        items = list(ShareChannel.objects.filter(date__range=(start_time, end_time), product=product, version=version,type=type).values_list('channel', flat=True).distinct())
        index = []
        for date in dates:
            index.append(date.strftime('%m-%d'))
            month_start = (date - datetime.timedelta(days=29)).strftime('%Y-%m-%d')
            res_temp = res.filter(date=date).order_by('count')
            temp = collections.OrderedDict()
            for item in res_temp:
                item_temp = {
                    'today': item.count
                }
                if mode == 'month':
                    month_res = ShareChannel.objects.filter(
                        date__range=(month_start, date.strftime('%Y-%m-%d')),
                        version=version,
                        type=type,
                        product=product,
                        channel=item.channel
                    ).values('channel').annotate(
                        count_total=Sum('count')
                    )
                    item_temp['month'] = month_res[0]['count_total']
                temp[item.channel] = item_temp
            data.append(temp)
        result = {
            'versions': versions,
            'data': data,
            'index': index,
            'items': items,
            'mode': mode
        }
        return JsonResponse(result, safe=False)
    else:
        return HttpResponse('Error.')

# bi系统->Nano内容分享->分享模式占比
@csrf_exempt
def share_mode(request):
    if request.method == 'POST':
        return HttpResponse('Task submitted.')
    elif request.method == 'GET':
        para = request.GET
        today = datetime.datetime.today()
        start_time = (today - datetime.timedelta(days=6)).strftime('%Y-%m-%d')
        end_time = (today + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        start_time = para.get('start_time', start_time)
        end_time = para.get('end_time', end_time)
        product = para.get('product_type', 'nano')
        version = para.get('version', 'all')

        data = []

        if version == 'all':
            if product == 'all':
                res = ShareMode.objects.filter(
                    date__range=(start_time, end_time)
                ).values(
                    'date', 'mode'
                ).annotate(
                    count=Sum('count')
                ).order_by('date')
                print res
            else:
                res = ShareMode.objects.filter(
                    date__range=(start_time, end_time), product=product,
                ).values(
                    'date','mode'
                ).annotate(
                    count=Sum('count')
                ).order_by('date')
        else:
            if product == 'all':
                res = ShareMode.objects.filter(
                    date__range=(start_time, end_time), version=version
                ).values(
                    'date', 'mode'
                ).annotate(
                    count=Sum('count')
                ).order_by('date')
            else:
                res = ShareMode.objects.filter(date__range=(start_time, end_time), product=product, version=version).order_by(
                'date').values()
        dates = res.dates('date', 'day')
        index = []
        for date in dates:
            index.append(date.strftime('%m-%d'))
            res_temp = res.filter(date=date).order_by('count')
            temp = collections.OrderedDict()
            for item in res_temp:
                temp[item['mode']] = item['count']
            data.append(temp)
        if product == 'all':
            versions = list(ShareMode.objects.values_list('version', flat=True).distinct())
        else:
            versions = list(ShareMode.objects.filter(product=product).values_list('version', flat=True).distinct())
        items = list(ShareMode.objects.filter(date__range=(start_time, end_time)).values_list('mode', flat=True).distinct())
        result = {
            'versions': versions,
            'data': data,
            'index': index,
            'items': items
        }
        return JsonResponse(result, safe=False)
    else:
        return HttpResponse('Error.')

#bi系统->Nano App使用情况->分享转化率
@csrf_exempt
def share_count(request):
    if request.method == 'POST':
        return HttpResponse('Task submitted.')
    elif request.method == 'GET':
        para = request.GET
        today = datetime.datetime.today()
        start_time = (today - datetime.timedelta(days=6)).strftime('%Y-%m-%d')
        end_time = (today + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        start_time = para.get('start_time', start_time)
        end_time = para.get('end_time', end_time)
        product = para.get('product_type', 'nano')
        version = para.get('version', 'all')
        type = para.get('type', 'img')
        data = []
        if version == 'all':
            res = ShareCount.objects.filter(
                date__range=(start_time, end_time),
                type=type,
                product=product
            ).values(
                'date'
            ).annotate(
                try_count=Sum('try_count'),
                success_count = Sum('success_count')
            ).order_by('date')
        else:
            res = ShareCount.objects.filter(date__range=(start_time, end_time), version=version, type=type,
                                            product=product).order_by('date').values()
        dates = res.dates('date', 'day')
        index = []
        for date in dates:
            index.append(date.strftime('%m-%d'))
            res_temp = res.filter(date=date).order_by('success_count')
            temp = collections.OrderedDict()
            for item in res_temp:
                try_count = item['try_count']
                success_count = item['success_count']
                if try_count == 0:
                    percent = 0
                else:
                    percent = round(success_count * 100.0 / try_count, 1)
                temp['share_count'] = try_count
                temp['success_count'] = success_count
                temp['percent'] = percent
            data.append(temp)
        versions = list(ShareCount.objects.filter(product=product).values_list('version',flat=True).distinct())
        result = {
            'data': data,
            'index': index,
            'versions': versions
        }
        return JsonResponse(result, safe=False)
    else:
        return HttpResponse('Error.')

#bi系统->Nano App使用情况->图片视频生产数
@csrf_exempt
def take_count(request):
    if request.method == 'POST':
        return HttpResponse('Task submitted.')
    elif request.method == 'GET':
        para = request.GET
        today = datetime.datetime.today()
        start_time = (today - datetime.timedelta(days=6)).strftime('%Y-%m-%d')
        end_time = (today + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        start_time = para.get('start_time', start_time)
        end_time = para.get('end_time', end_time)
        product = para.get('product_type', 'nano')
        version = para.get('version', 'all')
        data = []
        index = []
        if product == 'all':
            res = TakeCount.objects.filter(date__range=(start_time, end_time), version=version).values(
                'date'
            ).annotate(
                img_count=Sum('img_count'),
                video_count=Sum('video_count')
            ).order_by('date')
        else:
            res = TakeCount.objects.filter(date__range=(start_time, end_time), version=version,
                product=product).order_by('date').values()
        for item in res:
            index.append(item['date'].strftime('%m-%d'))
            temp = collections.OrderedDict()
            temp['img'] = item['img_count']
            temp['video'] = item['video_count']
            data.append(temp)
        if product == 'all':
            versions = list(TakeCount.objects.values_list('version', flat=True).distinct())
        else:
            versions = list(TakeCount.objects.filter(product=product).values_list('version', flat=True).distinct())
        result = {
            'data': data,
            'index': index,
            'versions': versions
        }
        return JsonResponse(result, safe=False)
    else:
        return HttpResponse('Error.')

#bi系统->Nano App使用情况->错误异常
@csrf_exempt
def error_condition(request):
    if request.method == 'POST':
        return HttpResponse('Task submitted.')
    elif request.method == 'GET':
        para = request.GET
        today = datetime.datetime.today()
        start_time = (today - datetime.timedelta(days=6)).strftime('%Y-%m-%d')
        end_time = (today + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        start_time = para.get('start_time', start_time)
        end_time = para.get('end_time', end_time)
        product = para.get('product_type', 'nano')
        if product == 'all':
            res = ErrorCondition.objects.filter(date__range=(start_time, end_time)).values(
                'date'
            ).annotate(
                total_error=Sum('total_error'),
                error_rate=Sum('error_rate')
            ).order_by('date')
        else:
            res = ErrorCondition.objects.filter(date__range=(start_time, end_time),
                product=product).order_by('date').values()
        data = []
        index = []
        for item in res:
            index.append(item['date'].strftime('%m-%d'))
            temp = {'date': item['date'].strftime('%m-%d'), 'total_error': item['total_error'], 'error_rate': item['error_rate']}
            data.append(temp)
        result = {
            'data': data,
            'index': index
        }
        return JsonResponse(result, safe=False)
    else:
        return HttpResponse('Error.')

#bi系统->Nano市场环境->搜索指数
@csrf_exempt
def market_environment(request):
    if request.method == 'POST':
        return HttpResponse('Task submitted.')
    elif request.method == 'GET':
        para = request.GET
        today = datetime.datetime.today()
        start_time = (today - datetime.timedelta(days=6)).strftime('%Y-%m-%d')
        end_time = (today + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        start_time = para.get('start_time', start_time)
        end_time = para.get('end_time', end_time)
        site = para.get('site', 'baidu')
        data = []
        index = []
        items = []
        if site == 'baidu':
            res = SearchIndex.objects.filter(date__range=(start_time, end_time)).order_by('date')
            dates = res.dates('date', 'day')
            for date in dates:
                index.append(date.strftime('%m-%d'))
                res_temp = res.filter(date=date)
                temp = {}
                items = list(res_temp.values_list('key', flat=True).distinct())
                for item in res_temp:
                    temp[item.key] = item.baidu_index
                data.append(temp)
        elif site == 'google':
            res = GoogleIndex.objects.filter(date__range=(start_time, end_time)).order_by('date')
            dates = res.dates('date', 'day')
            for date in dates:
                index.append(date.strftime('%m-%d'))
                res_temp = res.filter(date=date)
                temp = {}
                items = list(res_temp.values_list('key', flat=True).distinct())
                for item in res_temp:
                    temp[item.key] = item.google_index
                data.append(temp)
        result = {
            'data': data,
            'index': index,
            'items': items
        }
        return JsonResponse(result, safe=False)
    else:
        return HttpResponse('Error.')

#bi系统->新媒体监控->热度走势
@csrf_exempt
def media_data(request):
    if request.method == 'POST':
        return HttpResponse('Task submitted.')
    elif request.method == 'GET':
        para = request.GET
        today = datetime.datetime.today()
        start_time = (today - datetime.timedelta(days=6)).strftime('%Y-%m-%d')
        end_time = (today + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        start_time = para.get('start_time', start_time)
        end_time = para.get('end_time', end_time)
        platform = para.get('platform', 'facebook')

        items = {}
        items['instagram'] = ['comment', 'like']
        items['weixin'] = ['view', 'share']
        items['youku'] = ['comment', 'like', 'dislike', 'view']
        items['youtube'] = ['comment', 'like', 'dislike', 'view']
        items['twitter'] = ['like', 'share']
        items['weibo'] = ['comment', 'like', 'share']
        items['facebook'] = ['comment', 'like', 'share']
        items[u'腾讯视频'] = ['view']
        data = []
        index = []
        res = MediaData.objects.filter(date__range=(start_time, end_time), platform=platform).order_by('date')
        dates = res.dates('date', 'day')
        for date in dates:
            try:
                res_temp = res.get(date=date)
                index.append(date.strftime('%m-%d'))
            except:
                continue
            res_temp = model_to_dict(res_temp)
            temp = {}
            for item in items[platform]:
                temp[media_dict[item]] = res_temp[item]
            data.append(temp)
        platforms = list(MediaData.objects.values_list('platform', flat=True).distinct())
        indexes = []
        for item in items[platform]:
            indexes.append(media_dict[item])
        result = {
            'platform': platform,
            'platforms': platforms,
            'data': data,
            'items': indexes,
            'index': index
        }
        return JsonResponse(result, safe=False)
    else:
        return HttpResponse('Error.')

#bi系统->Nano市场环境->30天销量/评论
@csrf_exempt
def competitor_data(request):
    if request.method == 'POST':
        return HttpResponse('Task submitted.')
    elif request.method == 'GET':
        para = request.GET
        today = datetime.datetime.today()
        start_time = (today - datetime.timedelta(days=6)).strftime('%Y-%m-%d')
        end_time = (today + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        start_time = para.get('start_time', start_time)
        end_time = para.get('end_time', end_time)
        source = para.get('source', 'all')
        data = []
        index = []
        res = CompetitorSales.objects.filter(date__range=(start_time, end_time)).order_by('date')
        dates = res.dates('date', 'day')
        items = set()
        for date in dates:
            index.append(date.strftime('%m-%d'))
            res_temp = res.filter(date=date)
            temp = collections.OrderedDict()
            if source == 'all':
                for item in res_temp:
                    temp[item.commodity + ' 淘宝'] = item.taobao_total_sales
                    temp[item.commodity + ' 京东'] = item.jd_total_sales
                    items.add(item.commodity + ' 淘宝')
                    items.add(item.commodity + ' 京东')
            elif source == 'taobao':
                for item in res_temp:
                    temp[item.commodity + ' 淘宝'] = item.taobao_total_sales
                    items.add(item.commodity + ' 淘宝')
            elif source == 'jd':
                for item in res_temp:
                    temp[item.commodity + ' 京东'] = item.jd_total_sales
                    items.add(item.commodity + ' 京东')
            data.append(temp)
        items = list(items)
        result = {
            'data': data,
            'index': index,
            'items': items
        }
        return JsonResponse(result, safe=False)
    else:
        return HttpResponse('Error.')

# bi系统->Nano市场环境->30天销量/评论
@csrf_exempt
def competitor_sales(request):
    if request.method == 'POST':
        return HttpResponse('Task submitted.')
    elif request.method == 'GET':
        para = request.GET
        today = datetime.datetime.today()
        start_time = (today - datetime.timedelta(days=6)).strftime('%Y-%m-%d')
        end_time = (today + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        start_time = para.get('start_time', start_time)
        end_time = para.get('end_time', end_time)
        data = []
        index = []
        res = CompetitorSales.objects.filter(date__range=(start_time, end_time)).order_by('date')
        dates = res.dates('date', 'day')
        for date in dates:
            index.append(date.strftime('%m-%d'))
            month_age = (date - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
            res_temp = res.filter(date=date)
            temp = collections.OrderedDict()
            for item in res_temp:
                try:
                    month_age_res = CompetitorSales.objects.get(date=month_age, commodity=item.commodity)
                    jd_sales = item.jd_total_sales - month_age_res.jd_total_sales
                except:
                    jd_sales = int(item.jd_total_sales / 2)
                if jd_sales < 0:
                    jd_sales = 0
                temp[item.commodity] = item.taobao_total_sales + int(jd_sales / 0.15)
            data.append(temp)
        result = {
            'data': data,
            'index': index
        }
        return JsonResponse(result, safe=False)
    else:
        return HttpResponse('Error.')

#bi系统->Nano市场环境->亚马逊评论
@csrf_exempt
def global_sales(request):
    if request.method == 'POST':
        return HttpResponse('Task submitted.')
    elif request.method == 'GET':
        para = request.GET
        today = datetime.datetime.today()
        start_time = (today - datetime.timedelta(days=6)).strftime('%Y-%m-%d')
        end_time = (today + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        start_time = para.get('start_time', start_time)
        end_time = para.get('end_time', end_time)
        site = para.get('site', 'amazon')
        data = []
        index = []
        res = GlobalElectronicSales.objects.filter(date__range=(start_time, end_time), site=site)
        items = list(res.values_list('country', flat=True).distinct())
        res = res.order_by('date')
        dates = res.dates('date', 'day')
        for date in dates:
            index.append(date.strftime('%m-%d'))
            res_temp = res.filter(date=date).order_by('-comment')
            temp = collections.OrderedDict()
            for item in res_temp:
                temp[item.country] = item.comment
            data.append(temp)
        result = {
            'data': data,
            'index': index,
            'items': items
        }
        return JsonResponse(result, safe=False)
    else:
        return HttpResponse('Error.')

#bi系统->登录
@csrf_exempt
def login(request):
    if request.method == 'POST':
        return HttpResponse('Task submitted.')
    elif request.method == 'GET':
        para = request.GET
        username = 'jack'
        password = 'slow fuck'
        if para.__contains__('username'):
            username = para.__getitem__('username')
        if para.__contains__('password'):
            password = para.__getitem__('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                username = user.get_username()
                res = []
                groups = user.groups.all()
                for group in groups:
                    res.append(group.name)
                return JsonResponse({'result': True, 'username': username, 'group': res}, safe=False)
            else:
                return JsonResponse({'result': False}, safe=False)

        else:
            return JsonResponse({'result': False}, safe=False)
    else:
        return HttpResponse('Error.')

# bi系统->通过钉钉员工账号登录
@csrf_exempt
def dtalk_login(request):
    if request.method == 'POST':
        return HttpResponse('Task submitted.')
    elif request.method == 'GET':
        para = request.GET
        username = 'jack'
        password = 'slow fuck'
        if para.__contains__('username'):
            username = para.__getitem__('username')
        if para.__contains__('password'):
            password = para.__getitem__('password')
        url = 'http://account.arashivision.com/user/getUserToken'
        values = {
            'jobnumber': username,
            'password': password
        }
        data = urllib.urlencode(values)
        req = urllib2.Request(url=url, data=data)
        try:
            res_data = urllib2.urlopen(req)
        except urllib2.HTTPError, e:
            print e.code
            print e.reason
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                username = user.get_username()
                res = []
                groups = user.groups.all()
                for group in groups:
                    res.append(group.name)
                return JsonResponse({'result': True, 'username': username, 'group': res}, safe=False)
            else:
                return JsonResponse({'result': False}, safe=False)
        data = json.loads(res_data.read())
        jobnumber = data['jobNumber']
        name = data['name']
        try:
            user = User.objects.get(username=jobnumber)
            user.set_password(password)
            user.first_name = name
            user.save()
        except:
            user = User.objects.create_user(jobnumber, email=None, password=password)
            user.first_name = name
            user.save()
        res = []
        groups = user.groups.all()
        for group in groups:
            res.append(group.name)
        return JsonResponse({'result': True, 'username': name, 'group': res}, safe=False)
    else:
        return HttpResponse('Error.')

#bi系统->新媒体监控->粉丝走势
@csrf_exempt
def media_fans(request):
    if request.method == 'POST':
        return HttpResponse('Task submitted.')
    elif request.method == 'GET':
        para = request.GET
        today = datetime.datetime.today()
        start_time = (today - datetime.timedelta(days=6)).strftime('%Y-%m-%d')
        end_time = (today + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        start_time = para.get('start_time', start_time)
        end_time = para.get('end_time', end_time)
        type = para.get('type', 'total')
        data = []
        index = []
        start_temp = datetime.datetime.strptime(start_time, "%Y-%m-%d")
        start_time = (start_temp - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        res = MediaFan.objects.filter(date__range=(start_time, end_time)).order_by('date')
        items = list(res.values_list('platform', flat=True).distinct())
        res.order_by('date')
        dates = res.dates('date', 'day')
        count = 0
        for date in dates:
            if count > 0:
                index.append(date.strftime('%m-%d'))
            else:
                count += 1
            res_temp = res.filter(date=date).order_by('fans')
            temp = collections.OrderedDict()
            for item in res_temp:
                temp[item.platform] = item.fans
            data.append(temp)
        result = {
            'data': data,
            'index': index,
            'type': type,
            'items': items
        }
        return JsonResponse(result, safe=False)
    else:
        return HttpResponse('Error.')

# bi系统->新媒体监控->标签内容数走势
@csrf_exempt
def media_tag(request):
    if request.method == 'POST':
        return HttpResponse('Task submitted.')
    elif request.method == 'GET':
        para = request.GET
        today = datetime.datetime.today()
        start_time = (today - datetime.timedelta(days=6)).strftime('%Y-%m-%d')
        end_time = (today + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        start_time = para.get('start_time', start_time)
        end_time = para.get('end_time', end_time)
        data = []
        index = []
        start_temp = datetime.datetime.strptime(start_time, "%Y-%m-%d")
        start_time = (start_temp - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        res = MediaTag.objects.filter(date__range=(start_time, end_time)).order_by('date')
        dates = res.dates('date', 'day')
        count = 0
        for date in dates:
            if count > 0:
                index.append(date.strftime('%m-%d'))
            else:
                count += 1
            res_temp = res.filter(date=date).order_by('count')
            temp = collections.OrderedDict()
            for item in res_temp:
                temp[item.platform + '#' + item.tag] = item.count
            data.append(temp)
        result = {
            'data': data,
            'index': index
        }
        return JsonResponse(result, safe=False)
    else:
        return HttpResponse('Error.')

# bi系统->新媒体监控->Meltwater
@csrf_exempt
def meltwater(request):
    if request.method == 'POST':
        return HttpResponse('Task submitted.')
    elif request.method == 'GET':
        para = request.GET
        today = datetime.datetime.today()
        start_time = (today - datetime.timedelta(days=6)).strftime('%Y-%m-%d')
        end_time = (today + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        start_time = para.get('start_time', start_time)
        end_time = para.get('end_time', end_time)
        type = para.get('type', 'social')
        country = para.get('country', 'all')
        data = []
        index = []
        country_list = list(Meltwater.objects.filter().values_list('country', flat=True).distinct())

        if country == 'all':
            res = Meltwater.objects.filter(
                date__range=(start_time, end_time),
                type=type
            )
            items = list(res.values_list('key', flat=True).distinct())
            res = res.values(
                'date', 'key'
            ).annotate(
                value_total=Sum('value')
            ).order_by('date')
            country = '全部'
        else:
            res = Meltwater.objects.filter(date__range=(start_time, end_time), type=type, country=country)
            items = list(res.values_list('key', flat=True).distinct())
            res = res.order_by('date')
        dates = res.dates('date', 'day')
        for date in dates:
            index.append(date.strftime('%m-%d'))
            res_temp = res.filter(date=date).order_by('value')
            temp = collections.OrderedDict()
            for item in res_temp:
                temp[item['key']] = item['value_total']
            data.append(temp)
        result = {
            'data': data,
            'index': index,
            'items': items,
            'country': country,
            'type': type,
            'country_list': country_list
        }
        return JsonResponse(result, safe=False)
    else:
        return HttpResponse('Error.')

#bi系统->Nano市场环境->30天评论/销量->淘宝店铺详情
@csrf_exempt
def taobao_detail(request):
    if request.method == 'POST':
        return HttpResponse('Task submitted.')
    elif request.method == 'GET':
        para = request.GET
        today = datetime.datetime.today()
        date = (today - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        date = para.get('date', date)
        commodity = para.get('commodity', 'insta360 Nano')
        res = TaobaoDetail.objects.filter(
            date=date,
            commodity=commodity
        ).order_by('-sales')
        stores = []
        for item in res:
            temp = {
                'store_id': item.store_id,
                'shop': item.shop,
                'name': item.name,
                'price': item.price,
                'sales': item.sales,
                'link': item.link,
                'location': item.location,
                'is_tmall': item.is_tmall,
            }
            stores.append(temp)
        commodities_res = TaobaoDetail.objects.filter().values('commodity').distinct()
        commodities = []
        for c in commodities_res:
            commodities.append(c['commodity'])
        result = {'data': stores, 'commodities': commodities}
        return JsonResponse(result, safe=False)
    else:
        return HttpResponse('Error.')

#bi系统->Nano市场环境->30天评论/销量->淘宝店铺详情->单个店铺的销量走势
@csrf_exempt
def store_detail(request):
    if request.method == 'POST':
        return HttpResponse('Task submitted.')
    elif request.method == 'GET':
        para = request.GET
        if not para.__contains__('store_id'):
            return HttpResponse('Missing parameter store_id')
        store_id = para.__getitem__('store_id')
        today = datetime.datetime.today()
        start_time = (today - datetime.timedelta(days=29)).strftime('%Y-%m-%d')
        end_time = (today + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        start_time = para.get('start_time', start_time)
        end_time = para.get('end_time', end_time)
        res = TaobaoDetail.objects.filter(store_id=store_id, date__range=(start_time, end_time)).order_by('date')
        data = []
        index = []
        shop = ''
        for item in res:
            date = item.date
            index.append(date.strftime('%m-%d'))
            sales = item.sales
            shop = item.shop
            data.append(sales)
        result = {
            'data': data,
            'store': shop,
            'index': index
        }
        return JsonResponse(result, safe=False)

#用于本地调用测试
@csrf_exempt
def test(request):
    if request.method == 'POST':
        return HttpResponse('Task submitted.')
    elif request.method == 'GET':
        # get_fans()
        # get_media_data()
        get_google_index()
        # get_media_tag()
        return HttpResponse('success')
    else:
        return HttpResponse('Error.')
