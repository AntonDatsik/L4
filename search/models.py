from __future__ import unicode_literals

from django.db import models


class Page(models.Model):
    url = models.URLField(unique=True)

    def __unicode__(self):
        return self.url


class Word(models.Model):
    value = models.CharField(max_length=30, unique=True)
    pages = models.ManyToManyField(Page, through="Match")

    def __unicode__(self):
        return self.value


class Match(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    positions = models.CharField(max_length=100000)

    def __unicode__(self):
        return self.positions
