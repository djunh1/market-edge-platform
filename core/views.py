from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout

from users.models import CustomUser
from weekdayStudy.models import WeekdayStudy
from .forms import StudyForm
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
        Q(study__ticker__icontains=q))[0:5]

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
def updateStudy(request, pk):
    '''
    Probably won't allow updating of too many fields of studies.  Want a study to be mostly immutable
    so as to avoid hindsight bias
    '''
    study = Study.objects.get(id=pk)

    # pre fills a form with a specific instance

    pkForm = get_object_or_404(Study , pk=pk)
    form = StudyForm(instance=pkForm)

    if request.user != study.study_creator:
        return HttpResponseForbidden('Your are not allowed here!!')

    if request.method == 'POST':
        study.description = request.POST.get('description')
        study.save()
        return redirect('home')

    context = {'form': form}

    return render(request, 'weekdayStudy_form.html', context)

@login_required(login_url='login')
def deleteMessage(request, pk):
    '''
    Plot twist, we won't be allowing deletions of messages probably
    '''
    message = Message.objects.get(id=pk)

    if request.user != message.user:

        return HttpResponseForbidden('Unauthorized.')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'core/delete.html', {'obj': message})

