# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-11 21:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_delete_post'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleCounts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Article')),
            ],
        ),
    ]
