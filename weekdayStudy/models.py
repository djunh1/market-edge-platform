from django.db import models
from core.models import Study, StudyType
# Create your models here.

class WeekdayStudy(Study):
    study_type = models.ForeignKey(StudyType,
                                   default='WEEKDAY_STUDY',
                                   on_delete=models.SET_NULL,
                                   null=True)


