from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return HttpResponse("a placeholder")
    # studies = Study.objects.all()
    # context = {'studies': studies }
    # return render(request, 'main.html', context)

def study(request, pk):
    return HttpResponse("a placeholder")
    # studies = Study.objects.all()
    # context = {'studies': studies }
    # return render(request, 'main.html', context)
