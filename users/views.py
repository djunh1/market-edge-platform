from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from .models import CustomUser

from .forms import CustomUserCreationForm


class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "signup.html"


@login_required(login_url='login')
def updateUser(request):
    return HttpResponse("a placeholder")
    # user = request.user
    # form = UserForm(instance=user)

    # if request.method == 'POST':
    #     form = UserForm(request.POST, request.FILES, instance=user)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('user-profile', pk=user.id)

    # return render(request, 'base/update-user.html', {'form': form})

def userProfile(request, pk):
    user = CustomUser.objects.get(id=pk)
    studies = user.study_set.all()
    room_messages = user.message_set.all()
    context = {'user': user,
               'studies': studies,
               'room_messages': room_messages}
    return render(request, 'profile.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')
