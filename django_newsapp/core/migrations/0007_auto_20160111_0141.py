# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-11 01:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_article_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='description',
            field=models.CharField(default='', max_length=300),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='occupation',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]