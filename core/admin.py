from django.contrib import admin

# from .models import Study
from .models.models_study import CustomUser
from .models.models_message import Message


admin.site.register(Message)


