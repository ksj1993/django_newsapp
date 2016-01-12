# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-12 03:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_delete_articlecount'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleCount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=500)),
                ('title', models.CharField(max_length=300)),
                ('image_url', models.CharField(max_length=500)),
                ('image', models.ImageField(blank=True, upload_to='images')),
                ('site_name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=1000)),
                ('count', models.IntegerField(default=0)),
            ],
        ),
    ]
