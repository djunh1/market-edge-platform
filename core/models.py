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
    ticker = models.CharField(max_length=6)                         # (required) the ticker: tsla, nvda (pre populate or just add them)
    study_move_value = models.IntegerField(default=0)               # (optional) magnitude of move 4%, 10%
    study_move_volume = models.IntegerField(default=0)              # (optional) volume of move 1, 10, 20 in millions of shares (*10^6)
    study_date = models.DateField(null=True, blank=True)            # (required) The date the study was run for
    description = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']
        #abstract = True

    def __str__(self):
        return_string ='[{study_type}]-{ticker}__(move:{study_move_value}%) (volume:{study_move_volume} million)___{study_date})'.format(study_type=self.study_type,
                        ticker=self.ticker,
                        study_move_value=self.study_move_value,
                        study_move_volume=self.study_move_volume,
                        study_date=self.study_date)


        return return_string

class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    study = models.ForeignKey(Study, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]

    # Each study should be its own app.  Core will have all helper logic though, and this base Study to inherit



