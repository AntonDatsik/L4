from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible 
class Page(models.Model):
    url = models.URLField()

    def __str__(self):
        return self.url


@python_2_unicode_compatible 
class Word(models.Model):
    value = models.CharField(max_length=30, unique=True)
    pages = models.ManyToManyField(Page)

    def __str__(self):
        return self.value


@python_2_unicode_compatible 
class Match(models.Model):
    word = models.ForeignKey(Word)
    positions = models.CharField(max_length=100000)
    pageId = models.IntegerField()

    def __str__(self):
        return self.positions
