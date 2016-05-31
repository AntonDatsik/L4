from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

import os.path


def index(request):
	template = loader.get_template('index.html')
	app_dir = os.path.dirname(__file__)
	contest = { 'app_dir': app_dir }
	return HttpResponse(template.render(contest, request))