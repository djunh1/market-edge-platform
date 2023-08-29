from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import WeekdayStudy
from users.models import CustomUser


class WeekdayStudyForm(ModelForm):
    class Meta:
        model = WeekdayStudy
        fields = '__all__'
        exclude = ['study_creator']
