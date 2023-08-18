from django.db import models
from django.utils.translation import gettext as _


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
    study_type = models.ForeignKey(StudyType, on_delete=models.SET_NULL, null=True)
    ticker = models.CharField(max_length=6)                         # (required) the ticker: tsla, nvda (pre populate or just add them)
    type = models.CharField(max_length=20)                           # (required) type of study gap, move, eps, weekday  (foreign key?)
    study_move_value = models.IntegerField(blank=True, null=True)   # (optional) magnitude of move 4%, 10%
    study_move_volume = models.IntegerField(blank=True, null=True)  # (optional) volume of move 1, 10, 20 in millions of shares (*10^6)
    study_date = models.DurationField(null=True, blank=True)        # (required) The date the study was run for
    description = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    # maybe a user later...

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name

    # Each study should be its own app.  Core will have all helper logic though, and this base Study to inherit



