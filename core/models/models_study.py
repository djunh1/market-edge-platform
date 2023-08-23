import uuid

from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractUser

from users.models import CustomUser

# Should we do 1. Study Type -> study (general) -> study (specific)
# or           2. study(general) -> study(type) -> study(specific) ?

class StudyType(models.Model):
    WEEKDAY_STUDY = 'weekday_study'
    GAP_STUDY = 'gap_study'
    MOVE_STUDY = 'move study'
    FUNDAMENTALS_STUDY = 'fundamentals_study'
    EP_STUDY = 'ep_study'
    STATUS = [
       (WEEKDAY_STUDY, _('Analyze a stocks movements on a given week day')),
       (GAP_STUDY, _('Analyzes continuation gaps of a stock')),
       (MOVE_STUDY, _('Analyzes non-gap stock price movements')),
       (FUNDAMENTALS_STUDY, _('Company SEC 10q fundamentals')),
       (EP_STUDY, _('Episodic pivot')),
    ]

    status = models.CharField(
       max_length=32,
       choices=STATUS,
       default=WEEKDAY_STUDY,
    )

    def __str__(self):
        return self.status

class Study(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    study_creator = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    ticker = models.CharField(max_length=6)
    study_date_start = models.DateField(null=True, blank=True)
    study_date_end = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']
        #abstract = True

    def __str__(self):
        return_string ='[{study_type}]-{ticker}__({study_date_end})'.format(study_type=self.study_type,
                                                                        ticker=self.ticker,
                                                                        study_date_end=self.study_date_end)

        return return_string



