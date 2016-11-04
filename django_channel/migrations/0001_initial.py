# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-08 08:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChannelMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=32)),
                ('content', models.TextField()),
                ('destroy_time', models.DateTimeField(db_index=True)),
                ('created_time', models.DateTimeField(auto_now_add=True, db_index=True)),
            ],
        ),
    ]
