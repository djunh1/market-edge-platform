from django.shortcuts import render
from django.http import HttpResponse


# Fake, but the idea is to actually save various market edge studies and refer back to them somehow
studys = [
    { 'id':1, 'study_name': 'tsla-gap-4percent' },
    { 'id':2, 'study_name': 'nvda-weekday' },
    { 'id':3, 'study_name': 'csco-earnings-20230522' }

]

def home(request):
    return render(request, 'main.html')

def study(request):
    study = 1
    context = {'study': study}
    return render(request, 'core/study.html', context)

def blank_url(request):
    return HttpResponse("a placeholder")
