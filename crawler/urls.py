from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^sales_status/$', views.sales_status, name='sales_status'),
    url(r'^electronic_sales/$', views.electronic_sales, name='electronic_sales'),
    url(r'^user_distribution/$', views.user_distribution, name='user_distribution'),
    url(r'^use_condition/$', views.use_condition, name='use_condition'),
    url(r'^search_index/$', views.search_index, name='search_index'),
    url(r'^error_condition/$', views.error_condition, name='error_condition'),
    url(r'^test/$', views.test, name='test'),

]