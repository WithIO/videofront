# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-24 07:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pipeline', '0002_auto_20160824_0640'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Subtitles',
            new_name='Subtitle',
        ),
    ]