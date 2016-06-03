from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader, RequestContext

import os.path


def index(request):
	template = loader.get_template('index.html')
	context = RequestContext(request)
	return HttpResponse(template.render(context))
