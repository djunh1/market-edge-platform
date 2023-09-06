from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .models import WeekdayStudy
from .forms import WeekdayStudyEditForm
from core.models.models_message import Message
from users.models import CustomUser
from users.forms import CustomUserChangeForm

from .forms import WeekdayStudyForm

def home(request):
    return HttpResponse("a placeholder")


def study(request, pk):
    return HttpResponse("a placeholder")

@login_required(login_url='login')
def createWeekdayStudy(request):
    '''
    This will actually have to populate the data before saving it.  So lets
    Start by implementing a service to run but allow input (with defaults)
    So we can run the study on a specific stock.
    '''
    form = WeekdayStudyForm()

    if request.method == 'POST':
        WeekdayStudy.objects.create(
            study_creator=request.user,
            study_type=WeekdayStudy(study_type='WEEKDAY_STUDY'),
            ticker=request.POST.get('ticker'),
            description=request.POST.get('description'),
        )
        return redirect('home')

    context = {'form': form, 'study_type': "weekday_study"}
    return render(request, 'weekdayStudy_form.html', context)


# @login_required(login_url='login')
# def updateWeekdayStudy(request, pk):
#     '''
#     Probably won't allow updating of too many fields of studies.  Want a study to be mostly immutable
#     so as to avoid hindsight bias
#     '''
#     weekday_study = WeekdayStudy.objects.get(id=pk)

#     # pre fills a form with a specific instance
#     form = WeekdayStudy(instance=weekday_study)

#     if request.user != weekday_study.study_creator:
#         return HttpResponse('Your are not allowed here!!')

#     if request.method == 'POST':
#         weekday_study.description = request.POST.get('description')
#         weekday_study.save()
#         return redirect('home')


#     context = {'form': form}
#     return render(request, 'weekdayStudy_form.html', context)
