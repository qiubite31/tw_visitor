# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-09-28 09:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visitors', '0003_arrivalrecord'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Visitor',
        ),
        migrations.AddField(
            model_name='arrivalrecord',
            name='report_year',
            field=models.IntegerField(default=0, max_length=4),
        ),
        migrations.AlterField(
            model_name='arrivalrecord',
            name='report_month',
            field=models.IntegerField(default=0, max_length=2),
        ),
    ]
