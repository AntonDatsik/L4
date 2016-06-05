from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from search_engine.search_engine import SearchEngine


def index(request):
	search_engine = SearchEngine()
	search_engine.createIndex("https://google.com/")

	template = loader.get_template('index.html')
	context = RequestContext(request)
	return HttpResponse(template.render(context))
