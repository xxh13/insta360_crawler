# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


# Create your models here.

class UseCondition(models.Model):
    new_user = models.IntegerField(default=0)
    active_user = models.IntegerField(default=0)
    duration = models.IntegerField(default=0)
    date = models.DateField(auto_now=False, auto_now_add=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return str(self.id)


class SearchIndex(models.Model):
    key = models.CharField(max_length=200)
    baidu_index = models.IntegerField(default=0)
    date = models.DateField(auto_now=False, auto_now_add=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return str(self.id)

class GoogleIndex(models.Model):
    key = models.CharField(max_length=200)
    google_index = models.IntegerField(default=0)
    date = models.DateField(auto_now=False, auto_now_add=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return str(self.id)


class CompetitorSales(models.Model):
    commodity = models.CharField(max_length=200)
    taobao_sales = models.IntegerField(default=0)
    taobao_total_sales = models.IntegerField(default=0)
    jd_sales = models.IntegerField(default=0)
    jd_total_sales = models.IntegerField(default=0)
    date = models.DateField(auto_now=False, auto_now_add=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return str(self.id)


class AbroadSales(models.Model):
    commodity = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    comment = models.IntegerField(default=0)
    total_comment = models.IntegerField(default=0)
    site = models.CharField(max_length=200)
    date = models.DateField(auto_now=False, auto_now_add=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return str(self.id)


class UserDistribution(models.Model):
    location = models.CharField(max_length=200)
    active_user = models.IntegerField(default=0)
    active_rate = models.FloatField(default=0.0)
    new_user = models.IntegerField(default=0)
    new_rate = models.FloatField(default=0.0)
    launch_data = models.IntegerField(default=0)
    launch_rate = models.FloatField(default=0.0)
    date = models.DateField(auto_now=False, auto_now_add=False)
    is_native = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return str(self.id)


class ErrorCondition(models.Model):
    total_error = models.IntegerField(default=0)
    error_rate = models.FloatField(default=0.0)
    date = models.DateField(auto_now=False, auto_now_add=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return str(self.id)


class ShareChannel(models.Model):
    event_group_id = models.CharField(max_length=200, blank=True)
    channel = models.CharField(max_length=200, blank=True)
    type = models.CharField(max_length=200, blank=True)
    date = models.DateField(auto_now=False, auto_now_add=False)
    version = models.CharField(max_length=200, blank=True)
    count = models.IntegerField(default=0)
    device = models.IntegerField(default=0)
    count_per_launch = models.FloatField(default=0.0)
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return str(self.id)


class ShareCount(models.Model):
    type = models.CharField(max_length=200, blank=True)
    date = models.DateField(auto_now=False, auto_now_add=False)
    version = models.CharField(max_length=200, blank=True)
    success_count = models.IntegerField(default=0)
    success_device = models.IntegerField(default=0)
    success_count_per_launch = models.FloatField(default=0.0)
    try_count = models.IntegerField(default=0)
    try_device = models.IntegerField(default=0)
    try_count_per_launch = models.FloatField(default=0.0)
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return str(self.id)


class SalesStatus(models.Model):

    location = models.CharField(max_length=200)
    week = models.DateField(auto_now=False, auto_now_add=False)
    agent_name = models.CharField(max_length=200, blank=True)
    agent_type = models.CharField(max_length=200, blank=True)

    agent_price = models.IntegerField(default=0)
    pick_up = models.IntegerField(default=0)
    sales_online = models.IntegerField(default=0)
    sales_offline = models.IntegerField(default=0)
    sales_offline_count = models.IntegerField(default=0)
    inventory_first = models.IntegerField(default=0)
    inventory_lower = models.IntegerField(default=0)
    reject = models.IntegerField(default=0)
    is_native = models.IntegerField(default=0)

    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return str(self.id)


class ElectronicSales(models.Model):
    week = models.DateField(auto_now=False, auto_now_add=False)
    location = models.CharField(max_length=200)
    view = models.IntegerField(default=0)
    visitor = models.IntegerField(default=0)
    payment = models.FloatField(default=0.0)
    number = models.IntegerField(default=0)
    buyer = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return str(self.id)


class Log(models.Model):
    username = models.CharField(max_length=200)
    week = models.DateField(auto_now=False, auto_now_add=False)
    table = models.CharField(max_length=200)
    operator = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return str(self.id)


class MediaFan(models.Model):
    platform = models.CharField(max_length=200)
    fans_increment = models.IntegerField(default=0)
    fans = models.IntegerField(default=0)
    date = models.DateField(auto_now=False, auto_now_add=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return str(self.id)


class MediaData(models.Model):
    platform = models.CharField(max_length=200)
    date = models.DateField(auto_now=False, auto_now_add=False)
    comment = models.IntegerField(default=0)
    like = models.IntegerField(default=0)
    share = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)
    view = models.IntegerField(default=0)
    created_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateField(auto_now=True)

    def __unicode__(self):
        return str(self.id)


class TaobaoDetail(models.Model):
    shop = models.CharField(max_length=200)
    shop_keeper = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    commodity = models.CharField(max_length=200)
    price = models.FloatField(default=0.0)
    pay = models.IntegerField(default=0)
    sales = models.IntegerField(default=0)
    store_id = models.CharField(max_length=200)
    link = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    is_tmall = models.IntegerField(default=0)
    date = models.DateField(auto_now=False, auto_now_add=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return str(self.id)

# class Content(models.Model):
#     image = models.CharField(max_length=200)
#     video = models.CharField(max_length=200)
#     videoLength = models.CharField(max_length=200)
#     date = models.DateTimeField(max_length=200, unique=True)
#     date_created = models.DateTimeField(auto_now_add=True)
#     def __unicode__(self):
#         return str(self.date)
