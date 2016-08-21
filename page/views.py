from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'index/index.html', {
        'title': 'Index - Insta360 ',
        'msg': 'Internal System For Insta360.',
        'detail': 'HOOK / LOG / EMAIL.'
    })


def getLink(request):
    return render(request, 'get_link.html', {

    })