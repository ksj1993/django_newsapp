# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-09 15:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20160109_0141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='image',
            field=models.ImageField(blank=True, upload_to='images'),
        ),
    ]
