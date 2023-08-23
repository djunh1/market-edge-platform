from django.contrib import admin

# from .models import Study
from .models.models_study import StudyType
from .models.models_study import CustomUser


# admin.site.register(Study)
admin.site.register(StudyType)

