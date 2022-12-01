from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse('Starting a new project "Beauty services reservation platform"')
