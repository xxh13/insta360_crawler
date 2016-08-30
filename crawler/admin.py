from django.contrib import admin
from .models import UseCondition
from .models import SearchIndex
from .models import CompetitorSales
from .models import UserDistribution
from .models import SalesStatus
from .models import ElectronicSales
from .models import ErrorCondition
from .models import Log


# Register your models here.
class UseConditionAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'new_user', 'active_user', 'duration', 'date_created')


class SearchIndexAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'key', 'baidu_index', 'date_created')


class CompetitorSalesAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'commodity', 'taobao_sales',
                    'taobao_total_sales', 'jd_sales', 'jd_total_sales', 'date_created')


class UserDistributionAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'location',
                    'active_user', 'active_rate', 'new_user', 'new_rate', 'launch_data', 'launch_rate',
                    'is_native', 'date_created')


class ErrorConditionAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'total_error', 'date_created')


class SalesStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'week', 'location', 'pick_up',
                    'sales_online', 'sales_offline', 'inventory_first', 'inventory_lower',
                    'reject', 'is_native', 'date_created')


class ElectronicSalesAdmin(admin.ModelAdmin):
    list_display = ('id', 'week', 'location', 'view', 'visitor', 'payment', 'number', 'buyer', 'date_created')


class LogAdmin(admin.ModelAdmin):
    list_display = ('id', 'week', 'username', 'table', 'operator', 'location', 'date_created')


admin.site.register(UseCondition, UseConditionAdmin)
admin.site.register(SearchIndex, SearchIndexAdmin)
admin.site.register(CompetitorSales, CompetitorSalesAdmin)
admin.site.register(UserDistribution, UserDistributionAdmin)
admin.site.register(ErrorCondition, ErrorConditionAdmin)
admin.site.register(SalesStatus, SalesStatusAdmin)
admin.site.register(ElectronicSales, ElectronicSalesAdmin)
admin.site.register(Log, LogAdmin)
