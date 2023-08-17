from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'main.html')

def study(request):
    return HttpResponse("Specific stock study")

def blank_url(request):
    return HttpResponse("Placeholder")
