# coding=utf-8

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
from ..models import ElectronicPromotion
from ..models import AccessData
from ..models import Log
import datetime
import json
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

# 销售录入系统电商推广的增删该查接口
@csrf_exempt
def electronic_promotion(request):
    if request.method == 'POST':
        body = json.loads(request.body, encoding='utf-8')
        data = body['data']
        date = body['date']
        product = body['product']
        username = body['username']
        table = '电商推广'
        the_date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        next_day = (the_date + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        old = ElectronicPromotion.objects.filter(date=date, product=product).values('location')
        s = set()
        for item in old:
            s.add(item['location'])
        for item in data:
            result = ElectronicPromotion.objects.update_or_create(
                date=item['date'],
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
                week=item['date'],
                table=table,
                location=item['location'],
                operator=operator
            )
            ElectronicPromotion.objects.update_or_create(
                date=next_day,
                product=product,
                location=item['location']
            )
            if item['location'] in s:
                s.remove(item['location'])
        for i in s:
            ElectronicPromotion.objects.filter(date=date, location=i, product=product).delete()
            Log.objects.create(username=username, week=date, table=table, location=i, operator='delete')
        return HttpResponse('Task submitted.')
    elif request.method == 'GET':
        para = request.GET
        product = para.get('product', 'nano')
        date = datetime.datetime.today().strftime('%Y-%m-%d')
        if para.__contains__('date'):
            date = para.__getitem__('date')
        else:
            dates = ElectronicPromotion.objects.filter(product=product).dates('date', 'day', order='DESC')
            for item in dates:
                date = item.strftime('%Y-%m-%d')
                break
        data = []
        res = ElectronicPromotion.objects.filter(date=date, product=product)
        for item in res:
            temp = {
                'date': item.date,
                'location': item.location,
                'product': item.product,
                'show': item.show,
                'click': item.click,
                'cost': item.cost,
                'order': item.order,
                'turnover': item.turnover
            }
            data.append(temp)
        result = {'date': date, 'data': data}
        return JsonResponse(result, safe=False)
    else:
        return HttpResponse('Error.')


# 销售录入系统访问转化的增删该查接口
@csrf_exempt
def access_data(request):
    if request.method == 'POST':
        body = json.loads(request.body, encoding='utf-8')
        data = body['data']
        date = body['date']
        product = body['product']
        username = body['username']
        table = '访问转化'
        the_date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        next_day = (the_date + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        old = AccessData.objects.filter(date=date, product=product).values('location')
        s = set()
        for item in old:
            s.add(item['location'])
        for item in data:
            result = AccessData.objects.update_or_create(
                date=item['date'],
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
                week=item['date'],
                table=table,
                location=item['location'],
                operator=operator
            )
            AccessData.objects.update_or_create(
                date=next_day,
                product=product,
                location=item['location']
            )
            if item['location'] in s:
                s.remove(item['location'])
        for i in s:
            AccessData.objects.filter(date=date, location=i, product=product).delete()
            Log.objects.create(username=username, week=date, table=table, location=i, operator='delete')
        return HttpResponse('Task submitted.')
    elif request.method == 'GET':
        para = request.GET
        product = para.get('product', 'nano')
        date = datetime.datetime.today().strftime('%Y-%m-%d')
        if para.__contains__('date'):
            date = para.__getitem__('date')
        else:
            dates = AccessData.objects.filter(product=product).dates('date', 'day', order='DESC')
            for item in dates:
                date = item.strftime('%Y-%m-%d')
                break
        data = []
        res = AccessData.objects.filter(date=date, product=product)
        for item in res:
            temp = {
                'date': item.date,
                'location': item.location,
                'product': item.product,
                'view': item.view,
                'visitor': item.visitor,
                'customer': item.customer,
                'order': item.order
            }
            data.append(temp)
        result = {'date': date, 'data': data}
        return JsonResponse(result, safe=False)
    else:
        return HttpResponse('Error.')

#bi系统->Nano 零售渠道->电商推广
@csrf_exempt
def get_electronic_promotion(request):
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
        data = []
        index = []
        if location == 'all':
            res = ElectronicPromotion.objects.filter(
                date__range=(start_time, end_time),
                product__in=products
            )
        else:
            res = ElectronicPromotion.objects.filter(
                date__range=(start_time, end_time),
                location=location,
                product__in=products
            )
        res = res.values('date').annotate(
            show_total=Sum('show'),
            click_total=Sum('click'),
            cost_total=Sum('cost'),
            order_total=Sum('order'),
            turnover_total=Sum('turnover')).order_by('date')
        for item in res:
            temp = {
                'show': item['show_total'],
                'click': item['click_total'],
                'cost': item['cost_total'],
                'order': item['order_total'],
                'turnover': item['turnover_total']
            }
            index.append(item['date'].strftime('%m-%d'))
            data.append(temp)
        locations = list(ElectronicPromotion.objects.values_list('location', flat=True).distinct())
        products = list(ElectronicPromotion.objects.values_list('product', flat=True).distinct())
        result = {
            'locations': locations,
            'products': products,
            'data': data,
            'index': index
        }
        return JsonResponse(result, safe=False)
    else:
        return HttpResponse('Error.')


#bi系统->Nano 零售渠道->访问转化
@csrf_exempt
def get_access_data(request):
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
        data = []
        index = []
        if location == 'all':
            res = AccessData.objects.filter(
                date__range=(start_time, end_time),
                product__in=products
            )
        else:
            res = AccessData.objects.filter(
                date__range=(start_time, end_time),
                location=location,
                product__in=products
            )
        res = res.values('date').annotate(
            view_total=Sum('view'),
            visitor_total=Sum('visitor'),
            customer_total=Sum('customer'),
            order_total=Sum('order')).order_by('date')
        for item in res:
            temp = {
                'view': item['view_total'],
                'visitor': item['visitor_total'],
                'customer': item['customer_total'],
                'order': item['order_total']
            }
            index.append(item['date'].strftime('%m-%d'))
            data.append(temp)
        locations = list(AccessData.objects.values_list('location', flat=True).distinct())
        products = list(AccessData.objects.values_list('product', flat=True).distinct())
        result = {
            'locations': locations,
            'products': products,
            'data': data,
            'index': index
        }
        return JsonResponse(result, safe=False)
    else:
        return HttpResponse('Error.')