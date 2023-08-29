from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout

from users.models import CustomUser
from .models.models_study import Study
from .models.models_message import Message

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    studies = Study.objects.filter(
        Q(ticker__icontains=q) |
        Q(description__icontains=q)
    )

    study_count = studies.count()
    study_messages = Message.objects.filter(
        Q(study__ticker__icontains=q))[0:3]

    context = {'studies': studies, 'study_count': study_count, 'study_messages': study_messages}
    return render(request, 'base/home.html', context)

def study(request, pk):
    study = Study.objects.get(id=pk)
    study_messages = study.message_set.all()
    study_creator = study.study_creator

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            study=study,
            body=request.POST.get('body')
        )
        #study.participants.add(request.user)
        return redirect('study', pk=study.id)

    context = {'study': study, 'study_messages': study_messages, 'study_creator' :study_creator }
    return render(request, 'base/study.html', context)

@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('Unauthorized!!')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'core/delete.html', {'obj': message})

def blank_url(request):
    return HttpResponse("a placeholder")
