# coding=utf-8

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..models import VideoInfo
import datetime
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


# bi系统->新媒体监控->视频播放详情
@csrf_exempt
def video_info(request):
    if request.method == 'POST':
        return HttpResponse('Task submitted.')
    elif request.method == 'GET':
        para = request.GET
        platform = para.get('platform', 'youku')
        page = int(para.get('page', 1))
        if page < 1:
            page = 1
        per_page = int(para.get('per_page', 20))
        sort = para.get('sort', 'published_time|desc')
        temp = sort.split('|')
        sort = temp[0]
        sort_method = temp[1]
        if sort_method == 'desc':
            sort = '-' + sort
        temp = VideoInfo.objects.filter(platform=platform).latest('date')
        lastest_date = temp.date
        res = VideoInfo.objects.filter(platform=platform, date=lastest_date).order_by(sort)
        total = res.count()
        last_page = total / per_page + (1 if (total % per_page) > 0 else 0)
        if last_page <= 0:
            last_page = 1
        if page > last_page:
            page = last_page
        start = per_page * (page - 1)
        end = start + per_page
        if end > total:
            end = total
        if total == 0:
            videos = {}
        else:
            videos = res[start: end]
            videos = videos.values()
        data = []
        for video in videos:
            published_time = (video['published_time'] + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
            temp = {
                'id': video['video_id'],
                'platform': video['platform'],
                'title': video['title'],
                'comment': video['comment'],
                'like': video['like'],
                'dislike': video['dislike'],
                'view': video['view'],
                'duration': video['duration'],
                'link': video['link'],
                'thumb': video['thumb'],
                'published_time': published_time,
            }
            data.append(temp)
        platforms = list(VideoInfo.objects.values_list('platform', flat=True).distinct())
        pagination = {
            'total': total,
            'per_page': per_page,
            'current_page': page,
            'last_page': last_page,
            'from': start + 1,
            'to': end
        }
        result = {
            'links':{
                'pagination': pagination,
                'options': {
                    'platforms': platforms
                }
            },
            'data': data
        }
        return JsonResponse(result, safe=False)
    else:
        return HttpResponse('Error.')


# bi系统->新媒体监控->视频播放走势
@csrf_exempt
def video_trend(request):
    if request.method == 'POST':
        return HttpResponse('Task submitted.')
    elif request.method == 'GET':
        para = request.GET
        video_id = para.get('video_id', 'XMjczNDMyMTcxMg==')
        platform = para.get('platform', 'youku')
        today = datetime.datetime.today()
        start_time = (today - datetime.timedelta(days=29)).strftime('%Y-%m-%d')
        end_time = (today + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        start_time = para.get('start_time', start_time)
        end_time = para.get('end_time', end_time)
        start_temp = datetime.datetime.strptime(start_time, "%Y-%m-%d")
        start_time = (start_temp - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        res = VideoInfo.objects.filter(video_id=video_id, platform=platform, date__range=(start_time, end_time)).order_by('date')
        index = []
        view = []
        like = []
        dislike = []
        comment = []
        count = 0
        old_item = {}
        for item in res:
            if count == 0:
                count += 1
                old_item = item
                continue
            date = item.date
            index.append(date.strftime('%m-%d'))
            view.append(item.view - old_item.view)
            comment.append(item.comment - old_item.comment)
            like.append(item.like - old_item.like)
            dislike.append(item.dislike - old_item.dislike)
            old_item = item
        title = ''
        temp = VideoInfo.objects.filter(video_id=video_id, platform=platform).first()
        if temp != None:
            title = temp.title
        result = {
            'data': {
                'view': view,
                'like': like,
                'dislike': dislike,
                'comment': comment
            },
            'title': title,
            'index': index
        }
        return JsonResponse(result, safe=False)