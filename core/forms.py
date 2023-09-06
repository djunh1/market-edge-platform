from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models.models_study import Study

class StudyForm(ModelForm):
    class Meta:
        model = Study
        fields = '__all__'
        exclude = ['study_creator']
