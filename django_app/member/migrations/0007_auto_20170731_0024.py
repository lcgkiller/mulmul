# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-30 15:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0006_auto_20170730_2349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='nickname',
            field=models.CharField(max_length=15, unique=True),
        ),
    ]