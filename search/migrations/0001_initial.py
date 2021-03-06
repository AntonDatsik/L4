# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-04 12:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('positions', models.CharField(max_length=100000)),
                ('pageId', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(unique=True)),
                ('number_of_words', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='page',
            name='words',
            field=models.ManyToManyField(to='search.Word'),
        ),
        migrations.AddField(
            model_name='match',
            name='word',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search.Word'),
        ),
    ]
