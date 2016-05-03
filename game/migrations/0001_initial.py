# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-28 10:34
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dimen', models.IntegerField(null=True)),
                ('timeGap', models.IntegerField(default=3)),
                ('isFinished', models.BooleanField(default=False)),
                ('isStarted', models.BooleanField(default=True)),
                ('timeCreated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.IntegerField(choices=[(0, 'ZERO'), (1, 'ONE'), (2, 'TWO'), (3, 'THREE'), (4, 'FOUR'), (5, 'FIVE'), (6, 'SIX'), (7, 'SEVEN'), (8, 'EIGHT'), (9, 'NINE')], default=0)),
                ('firstName', models.CharField(max_length=30)),
                ('lastName', models.CharField(max_length=30)),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='users',
            field=models.ManyToManyField(to='game.Profile'),
        ),
    ]