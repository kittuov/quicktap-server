# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-30 16:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_auto_20160430_1449'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='total',
            field=models.IntegerField(default=0),
        ),
    ]
