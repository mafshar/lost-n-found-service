# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-03 04:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lostnfound', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='found',
            field=models.BooleanField(default=None, verbose_name=b'Found'),
        ),
    ]
