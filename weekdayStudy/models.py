from django.db import models
from core.models import Study
# Create your models here.

class WeekdayStudy(Study):
    a_field = models.TextField(null=True, blank=True)
