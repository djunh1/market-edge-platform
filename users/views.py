from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required

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
