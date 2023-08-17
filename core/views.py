from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("The Desk")

def study(request):
    return HttpResponse("Specific stock study")
