# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-04-10 13:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("pipeline", "0013_auto_20180124_0930")]

    operations = [
        migrations.AlterModelOptions(name="videoformat", options={"ordering": ["id"]})
    ]
