# coding=utf-8

from django.conf.urls import url
from . import views
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
urlpatterns = [
    #销售录入系统的增删该查接口
    url(r'^sales_status/$', views.sales_status, name='sales_status'),

    # 销售录入系统电商销售的增删该查接口
    url(r'^electronic_sales/$', views.electronic_sales, name='electronic_sales'),

    # bi系统->Nano 零售渠道->国内、海外销售情况
    url(r'^get_sales_status/$', views.get_sales_status, name='get_sales_status'),

    # bi系统->Nano 零售渠道->自有电商渠道
    url(r'^get_electronic_sales/$', views.get_electronic_sales, name='get_electronic_sales'),

    # bi系统->Nano App使用情况->APP用户区域分布
    url(r'^user_distribution/$', views.user_distribution, name='user_distribution'),

    # bi系统->Nano App使用情况->APP用户区域分布->区域对比
    url(r'^user_area/$', views.user_area, name='user_area'),

    # bi系统->Nano App使用情况->用户概况
    url(r'^use_condition/$', views.use_condition, name='use_condition'),

    # bi系统->Nano App使用情况->错误异常
    url(r'^error_condition/$', views.error_condition, name='error_condition'),

    # bi系统->Nano内容分享->分享渠道占比
    url(r'^share_channel/$', views.share_channel, name='share_channel'),

    # bi系统->Nano内容分享->分享模式占比
    url(r'^share_mode/$', views.share_mode, name='share_mode'),

    # bi系统->Nano App使用情况->分享转化率
    url(r'^share_count/$', views.share_count, name='share_count'),

    # bi系统->Nano App使用情况->图片视频生产数
    url(r'^take_count/$', views.take_count, name='take_count'),

    # bi系统->Nano市场环境->搜索指数
    url(r'^market_environment/$', views.market_environment, name='market_environment'),

    # bi系统->Nano市场环境->30天销量/评论
    url(r'^competitor_data/$', views.competitor_data, name='competitor_data'),

    # bi系统->Nano市场环境->30天销量/评论
    url(r'^competitor_sales/$', views.competitor_sales, name='competitor_sales'),

    # bi系统->Nano市场环境->亚马逊评论
    url(r'^global_sales/$', views.global_sales, name='global_sales'),

    # bi系统->新媒体监控->粉丝走势
    url(r'^media_fans/$', views.media_fans, name='media_fans'),

    # bi系统->新媒体监控->热度走势
    url(r'^media_data/$', views.media_data, name='media_data'),

    # bi系统->新媒体监控->标签内容数走势
    url(r'^media_tag/$', views.media_tag, name='media_tag'),

    # bi系统->新媒体监控->Meltwater
    url(r'^meltwater/$', views.meltwater, name='meltwater'),

    # bi系统->新媒体监控->视频播放信息
    url(r'^video_info/$', views.video_info, name='video_info'),

    # bi系统->新媒体监控->视频播放信息->视频数据趋势
    url(r'^video_trend/$', views.video_trend, name='video_trend'),

    # bi系统->Nano市场环境->30天评论/销量->淘宝店铺详情
    url(r'^taobao_detail/$', views.taobao_detail, name='taobao_detail'),

    # bi系统->Nano市场环境->30天评论/销量->淘宝店铺详情->单个店铺的销量走势
    url(r'^store_detail/$', views.store_detail, name='store_detail'),

    # bi系统->登录
    url(r'^login/$', views.login, name='login'),

    # bi系统->dtalk登录
    url(r'^dtalk_login/$', views.dtalk_login, name='dtalk_login'),

    # 权限控制后台
    url(r'^admin/power$', views.admin_power, name='admin_power'),

    # 权限控制后台登录
    url(r'^admin/login$', views.admin_login, name='admin_login'),

    url(r'^test/$', views.test, name='test'),

]