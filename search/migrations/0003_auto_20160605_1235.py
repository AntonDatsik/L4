# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-05 12:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0002_auto_20160604_1935'),
    ]

    operations = [
        migrations.RenameField(
            model_name='match',
            old_name='pageId',
            new_name='page_id',
        ),
    ]