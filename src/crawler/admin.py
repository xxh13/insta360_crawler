from django.contrib import admin
from .models import UseCondition
from .models import SearchIndex
from .models import GoogleIndex
from .models import CompetitorSales
from .models import UserDistribution
from .models import SalesStatus
from .models import ElectronicSales
from .models import ErrorCondition
from .models import ShareChannel
from .models import ShareMode
from .models import ShareCount
from .models import TakeCount
from .models import Log
from .models import MediaFan
from .models import MediaData
from .models import VideoInfo
from .models import MediaTag
from .models import TaobaoDetail
from .models import GlobalElectronicSales
from .models import Meltwater


# Register your models here.
class UseConditionAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'date', 'new_user', 'active_user', 'duration', 'date_created')


class SearchIndexAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'key', 'baidu_index', 'date_created')


class GoogleIndexAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'key', 'google_index', 'date_created')


class CompetitorSalesAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'commodity', 'taobao_sales',
                    'taobao_total_sales', 'jd_sales', 'jd_total_sales', 'date_created')


class UserDistributionAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'date', 'location',
                    'active_user', 'active_rate', 'new_user',
                    'new_rate', 'launch_data', 'launch_rate',
                    'is_native', 'date_created')


class ErrorConditionAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'date', 'total_error', 'error_rate', 'date_created')


class ShareChannelAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'event_group_id', 'channel', 'type', 'date',
                    'version', 'count', 'device', 'count_per_launch', 'date_created')


class ShareModeAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'event_group_id', 'mode', 'date',
                    'version', 'count', 'device', 'count_per_launch', 'date_created')

class ShareCountAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'type', 'date',
                    'version', 'success_count', 'success_device',
                    'success_count_per_launch', 'try_count', 'try_device',
                    'try_count_per_launch', 'date_created')

class TakeCountAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'date', 'version', 'img_count', 'img_device','img_count_per_launch', 'video_count', 'video_device','video_count_per_launch', 'created_time', 'update_time')

class SalesStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'week', 'location', 'pick_up',
                    'agent_name', 'agent_type', 'agent_price',
                    'sales_online', 'sales_offline', 'sales_offline_count',
                    'inventory_first', 'inventory_lower',
                    'reject', 'is_native', 'date_created')


class ElectronicSalesAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'week', 'location', 'view', 'visitor',
                    'payment', 'number', 'buyer', 'date_created')


class LogAdmin(admin.ModelAdmin):
    list_display = ('id', 'week', 'username', 'table', 'operator', 'location', 'date_created')

class MediaFanAdmin(admin.ModelAdmin):
    list_display = ('id', 'platform', 'fans_increment', 'fans', 'date', 'date_created')

class MediaDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'platform', 'date', 'comment', 'like', 'dislike', 'share', 'view', 'created_time', 'update_time')

class VideoInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'platform', 'video_id', 'title', 'date', 'comment', 'like', 'dislike', 'view', 'duration', 'link', 'thumb', 'published_time', 'created_time', 'update_time')

class MediaTagAdmin(admin.ModelAdmin):
    list_display = ('id', 'platform', 'tag', 'count', 'date', 'created_time', 'update_time')

class TaobaoDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'shop', 'shop_keeper',
                    'name', 'commodity', 'price',
                    'pay', 'sales', 'store_id', 'link',
                    'location', 'is_tmall', 'date', 'date_created')

class GlobalElectronicSalesAdmin(admin.ModelAdmin):
    list_display = ('id', 'commodity', 'site', 'country', 'comment', 'sale', 'date', 'created_time', 'update_time')

class MeltwaterAdmin(admin.ModelAdmin):
    list_display = ('id', 'key', 'type', 'country', 'value', 'date', 'created_time', 'update_time')

admin.site.register(UseCondition, UseConditionAdmin)
admin.site.register(SearchIndex, SearchIndexAdmin)
admin.site.register(GoogleIndex, GoogleIndexAdmin)
admin.site.register(CompetitorSales, CompetitorSalesAdmin)
admin.site.register(UserDistribution, UserDistributionAdmin)
admin.site.register(ErrorCondition, ErrorConditionAdmin)
admin.site.register(ShareChannel, ShareChannelAdmin)
admin.site.register(ShareMode, ShareModeAdmin)
admin.site.register(ShareCount, ShareCountAdmin)
admin.site.register(TakeCount, TakeCountAdmin)
admin.site.register(SalesStatus, SalesStatusAdmin)
admin.site.register(ElectronicSales, ElectronicSalesAdmin)
admin.site.register(Log, LogAdmin)
admin.site.register(MediaFan, MediaFanAdmin)
admin.site.register(MediaData, MediaDataAdmin)
admin.site.register(MediaTag, MediaTagAdmin)
admin.site.register(VideoInfo, VideoInfoAdmin)
admin.site.register(TaobaoDetail, TaobaoDetailAdmin)
admin.site.register(GlobalElectronicSales, GlobalElectronicSalesAdmin)
admin.site.register(Meltwater, MeltwaterAdmin)