from __future__ import unicode_literals

from django.db import models

# Create your models here.




class Page(models.Model):
	url = models.URLField()

class Word(models.Model):
	value = models.CharField(max_length=30, unique=True)
	pages = models.ManyToManyField(Page)

class Match(models.Model):
	word = models.ForeignKey(Word)
	positions = models.CharField(max_length=100000)
	pageId = models.IntegerField()
