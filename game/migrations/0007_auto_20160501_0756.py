# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-01 07:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0006_profile_ws_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='isStarted',
            field=models.BooleanField(default=False),
        ),
    ]