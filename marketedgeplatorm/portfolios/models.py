from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _
from users.models import Profile

class Portfolio(models.Model):
    owner = models.ForeignKey(
        Profile, null=True, blank=True, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    tags = models.ManyToManyField('Tag',  blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    LONG_TERM_VALUE = 'Long term value investing'
    GROWTH_INVESTING = 'Growth investing, short to long term'
    SWING_TRADE = 'Swing trade, short term'
    ETF_INVESTOR = ''
    PORTOFLIO_OPTIONS = [
        (LONG_TERM_VALUE, _('Long Term Value - Buy and hold for months or years')),
        (GROWTH_INVESTING, _('Growth Investing - Holding higher growth and momentum stocks')),
        (SWING_TRADE, _('Swing Trading - Hold periods of weeks to months')),
    ]

    portfolio_type = models.CharField(
       max_length=200,
       choices=PORTOFLIO_OPTIONS,
       default=LONG_TERM_VALUE
    )

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('owner__id', flat=True)
        return queryset

    # Won't use this yet. It may be helpful to vote on portfolios later on, if nothing else than 
    # for sentiment checks
    # @property
    # def getVoteCount(self):
    #     reviews = self.review_set.all()
    #     upVotes = reviews.filter(value='up').count()
    #     totalVotes = reviews.count()

    #     ratio = (upVotes / totalVotes) * 100
    #     self.vote_total = totalVotes
    #     self.vote_ratio = ratio

    #     self.save()


class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote'),
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    # One comment on a portfolio per user
    # class Meta:
    #     unique_together = [['owner', 'portfolio']]

    def __str__(self):
        return self.value
    
    class Meta:
        ordering = ['-created']
    
class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    



    
    

