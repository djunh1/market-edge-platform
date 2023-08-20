from django.shortcuts import render
from django.http import HttpResponse

from .models import Study

def home(request):
    return HttpResponse("a placeholder")
    # studies = Study.objects.all()
    # context = {'studies': studies }
    # return render(request, 'main.html', context)

def study(request, pk):
    return HttpResponse("a placeholder")
    # study = Study.objects.get(id=pk)
    # context = {'study': study}
    # return render(request, 'core/study.html', context)
    # Will probably delete.  Maybe can use as base view?  not sure yet.  

def blank_url(request):
    return HttpResponse("a placeholder")
