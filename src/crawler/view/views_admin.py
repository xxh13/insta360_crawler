# coding=utf-8

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import Group
from ..util.dict import group_dict
import sys
import urllib
import urllib2
import requests

reload(sys)
sys.setdefaultencoding('utf-8')


@csrf_exempt
def admin_login(request):
    if request.method == 'GET':
        return render(request, 'admin/myLogin.html', {})
    if request.method == 'POST':
        para = request.POST

        if para.__contains__('username'):
            username = para.__getitem__('username')
        else:
            return HttpResponse("Missing parameter: username")

        if para.__contains__('password'):
            password = para.__getitem__('password')
        else:
            return HttpResponse("Missing parameter: password")

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
            return HttpResponse(content='账号或密码错误！')
        status = res_data.code
        if status == 200:
            try:
                user = User.objects.get(username=username)
            except:
                return HttpResponse(content='抱歉，你没有权限登录', status=status)
            if user.is_superuser:
                request.session['bi_admin_id'] = username
                return HttpResponse(content='success', status=status)
            else:
                return HttpResponse(content='抱歉，你没有权限登录！', status=status)
        else:
            return HttpResponse(content='账号或密码错误！', status=status)


@csrf_exempt
def admin_power(request):
    if request.method == 'GET':
        if not request.session.__contains__('bi_admin_id'):
            return redirect('/crawler/admin/login')
        job_number = ""
        flag = 0
        para = request.GET
        if para.__contains__('job_number'):
            job_number = para.__getitem__('job_number')
        if job_number == "":
            return render(request, 'admin/power.html', {
                'flag': flag
            })
        flag = 1
        groups_all = Group.objects.all()
        try:
            user = User.objects.get(username=job_number)
            user_groups = user.groups.all()
        except:
            user = {}
            user_groups = {}
        groups = []
        for group in groups_all:
            group_name = group.name
            if group in user_groups:
                temp = {
                    'name': group_name,
                    'value': True,
                    'remark': group_dict[group_name]
                }
            else:
                temp = {
                    'name': group_name,
                    'value': False,
                    'remark': group_dict[group_name]
                }
            groups.append(temp)
        return render(request, 'admin/power.html', {
            'job_number': job_number,
            'groups': groups,
            'user': user,
            'flag': flag
        })
    if request.method == 'POST':
        para = request.POST
        job_number = para.__getitem__('job_number')
        try:
            user = User.objects.get(username=job_number)
        except:
            user = User.objects.create_user(job_number, email=None, password='jackslowfuck')
        user.groups.clear()
        for index in para:
            if index != 'job_number':
                value = para.__getitem__(index)
                if value == 'true':
                    try:
                        group = Group.objects.get(name=index)
                        user.groups.add(group)
                    except:
                        pass
                    if index == 'nano_sales':
                        data = {
                            'job_number': job_number,
                            'bi': 1
                        }
                        requests.post('http://sales.internal.insta360.com/sales/admin/power_update', data)
        user.save()
        return HttpResponse('success')