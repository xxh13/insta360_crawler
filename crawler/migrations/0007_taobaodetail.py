# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-30 03:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0006_auto_20160928_1847'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaobaoDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shop', models.CharField(max_length=200)),
                ('shop_keeper', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=200)),
                ('price', models.FloatField(default=0.0)),
                ('pay', models.IntegerField(default=0)),
                ('sales', models.IntegerField(default=0)),
                ('store_id', models.CharField(max_length=200)),
                ('link', models.CharField(max_length=200)),
                ('location', models.CharField(max_length=200)),
                ('is_tmall', models.IntegerField(default=0)),
                ('date', models.DateField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
