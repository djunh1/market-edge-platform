import uuid

from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


from users.models import CustomUser

# validators

def validate_study_types(value):

    if ('weekday_study' in value or
        'gap_study' in value or
        'move_study' in value or
        'fundamentals_study' in value or
        'ep_study' in value) :
        return value
    else:
        raise ValidationError("This field accepts only a specific study")

# Maybe add stock or company models too.  But for now we will use the ticker in these models for simplicity
class Study(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    study_creator = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    # Maybe participants of the study later,
    # IE participants = models.ManyToManyField( User, related_name='participants', blank=True)
    ticker = models.CharField(max_length=6)
    study_date_start = models.DateField(null=True, blank=True)
    study_date_end = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    WEEKDAY_STUDY = 'weekday_study'
    GAP_STUDY = 'gap_study'
    MOVE_STUDY = 'move_study'
    FUNDAMENTALS_STUDY = 'fundamentals_study'
    EP_STUDY = 'ep_study'
    STUDY_OPTIONS = [
       (WEEKDAY_STUDY, _('WEEKDAY STUDY - Analyzes how a stock moves daily on any day of the week.')),
       (GAP_STUDY, _('GAP STUDY - Analyzes continuation gaps of a stock on a given day')),
       (MOVE_STUDY, _('MOVE STUDY - Analyzes non-gap stock price movements on a given day')),
       (FUNDAMENTALS_STUDY, _('FUNDAMENTAL SNAPSHOT - Company SEC 10q fundamentals, rates of growth, and forecast for a specific date')),
       (EP_STUDY, _('EPISODIC PIVOT - there can be only one')), # Honestly this will probably just be a gap study
    ]

    study_type = models.CharField(
       max_length=32,
       choices=STUDY_OPTIONS,
       default=WEEKDAY_STUDY,
       validators=[validate_study_types]
    )

    class Meta:
        ordering = ['-updated', '-created']
        #abstract = True

    def __str__(self):
        return_string ='[{study_type}]-{ticker}__({study_date_end})'.format(study_type=self.study_type,
                                                                        ticker=self.ticker,
                                                                        study_date_end=self.study_date_end)

        return return_string



