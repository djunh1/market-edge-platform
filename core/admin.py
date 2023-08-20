from django.contrib import admin

from .models import Study
from .models import StudyType
from .models import User


admin.site.register(Study)
admin.site.register(StudyType)
admin.site.register(User)
