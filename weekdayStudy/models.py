from django.db import models
from core.models.models_study import Study, StudyType

DAYS_OF_WEEK = (
    (0, 'Monday'),
    (1, 'Tuesday'),
    (2, 'Wednesday'),
    (3, 'Thursday'),
    (4, 'Friday'),
    (5, 'Saturday'),
    (6, 'Sunday'),
)

class WeekdayStudy(Study):
    study_type = models.ForeignKey(StudyType,
                                   default='WEEKDAY_STUDY',
                                   on_delete=models.SET_NULL,
                                   null=True)

    '''
    A little brutal but lets just run with it for now
    '''

    # Manic Monday
    chg_today_count_up_monday = models.IntegerField(default=0)
    chg_today_count_down_monday = models.IntegerField(default=0)
    chg_today_magnitude_monday = models.FloatField(default=0)
    chg_today_magnitude_mean_monday = models.FloatField(default=0)
    chg_today_magnitude_std_monday = models.FloatField(default=0)
    chg_today_percent_monday = models.FloatField(default=0)
    chg_today_percent_mean_monday = models.FloatField(default=0)
    chg_today_percent_std_monday = models.FloatField(default=0)
    #Change from yesterday
    chg_from_yest_count_up_monday = models.IntegerField(default=0)
    chg_from_yest_count_down_monday = models.IntegerField(default=0)
    chg_from_yest_magnitude_monday = models.FloatField(default=0)
    chg_from_yest_magnitude_mean_monday = models.FloatField(default=0)
    chg_from_yest_magnitude_std_monday = models.FloatField(default=0)
    chg_from_yest_percent_monday = models.FloatField(default=0)
    chg_from_yest_percent_mean_monday = models.FloatField(default=0)
    chg_from_yest_percent_std_monday = models.FloatField(default=0)

    # Week performance
    total_weeks_monday = models.IntegerField(default=0)
    day_up_week_up_odds_monday = models.FloatField(default=0)
    day_up_week_up_pct_monday = models.FloatField(default=0)
    day_up_week_up_pct_mean_monday = models.FloatField(default=0)
    day_up_week_up_pct_std_monday = models.FloatField(default=0)
    day_up_week_up_magnitude_monday = models.FloatField(default=0)
    day_up_week_up_magnitude_mean_monday = models.FloatField(default=0)
    day_up_week_up_magnitude_std_monday = models.FloatField(default=0)

    day_up_week_down_odds_monday = models.FloatField(default=0)
    day_up_week_down_pct_monday = models.FloatField(default=0)
    day_up_week_down_pct_mean_monday = models.FloatField(default=0)
    day_up_week_down_pct_std_monday = models.FloatField(default=0)
    day_up_week_down_magnitude_monday = models.FloatField(default=0)
    day_up_week_down_magnitude_mean_monday = models.FloatField(default=0)
    day_up_week_down_magnitude_std_monday = models.FloatField(default=0)

    day_down_week_up_odds_monday = models.FloatField(default=0)
    day_down_week_up_pct_monday = models.FloatField(default=0)
    day_down_week_up_pct_mean_monday = models.FloatField(default=0)
    day_down_week_up_pct_std_monday = models.FloatField(default=0)
    day_down_week_up_magnitude_monday = models.FloatField(default=0)
    day_down_week_up_magnitude_mean_monday = models.FloatField(default=0)
    day_down_week_up_magnitude_std_monday = models.FloatField(default=0)

    day_down_week_down_odds_monday = models.FloatField(default=0)
    day_down_week_down_pct_monday = models.FloatField(default=0)
    day_down_week_down_pct_mean_monday = models.FloatField(default=0)
    day_down_week_down_pct_std_monday = models.FloatField(default=0)
    day_down_week_down_magnitude_monday = models.FloatField(default=0)
    day_down_week_down_magnitude_mean_monday = models.FloatField(default=0)
    day_down_week_down_magnitude_std_monday = models.FloatField(default=0)

    # Two fer Tuesday
    chg_today_count_up_tuesday = models.IntegerField(default=0)
    chg_today_count_down_tuesday = models.IntegerField(default=0)
    chg_today_magnitude_tuesday = models.FloatField(default=0)
    chg_today_magnitude_mean_tuesday = models.FloatField(default=0)
    chg_today_magnitude_std_tuesday = models.FloatField(default=0)
    chg_today_percent_tuesday = models.FloatField(default=0)
    chg_today_percent_mean_tuesday = models.FloatField(default=0)
    chg_today_percent_std_tuesday = models.FloatField(default=0)
    #Change from yesterday
    chg_from_yest_count_up_tuesday = models.IntegerField(default=0)
    chg_from_yest_count_down_tuesday = models.IntegerField(default=0)
    chg_from_yest_magnitude_tuesday = models.FloatField(default=0)
    chg_from_yest_magnitude_mean_tuesday = models.FloatField(default=0)
    chg_from_yest_magnitude_std_tuesday = models.FloatField(default=0)
    chg_from_yest_percent_tuesday = models.FloatField(default=0)
    chg_from_yest_percent_mean_tuesday = models.FloatField(default=0)
    chg_from_yest_percent_std_tuesday = models.FloatField(default=0)

    # Week performance
    total_weeks_tuesday = models.IntegerField(default=0)
    day_up_week_up_odds_tuesday = models.FloatField(default=0)
    day_up_week_up_pct_tuesday = models.FloatField(default=0)
    day_up_week_up_pct_mean_tuesday = models.FloatField(default=0)
    day_up_week_up_pct_std_tuesday = models.FloatField(default=0)
    day_up_week_up_magnitude_tuesday = models.FloatField(default=0)
    day_up_week_up_magnitude_mean_tuesday = models.FloatField(default=0)
    day_up_week_up_magnitude_std_tuesday = models.FloatField(default=0)

    day_up_week_down_odds_tuesday = models.FloatField(default=0)
    day_up_week_down_pct_tuesday = models.FloatField(default=0)
    day_up_week_down_pct_mean_tuesday = models.FloatField(default=0)
    day_up_week_down_pct_std_tuesday = models.FloatField(default=0)
    day_up_week_down_magnitude_tuesday = models.FloatField(default=0)
    day_up_week_down_magnitude_mean_tuesday = models.FloatField(default=0)
    day_up_week_down_magnitude_std_tuesday = models.FloatField(default=0)

    day_down_week_up_odds_tuesday = models.FloatField(default=0)
    day_down_week_up_pct_tuesday = models.FloatField(default=0)
    day_down_week_up_pct_mean_tuesday = models.FloatField(default=0)
    day_down_week_up_pct_std_tuesday = models.FloatField(default=0)
    day_down_week_up_magnitude_tuesday = models.FloatField(default=0)
    day_down_week_up_magnitude_mean_tuesday = models.FloatField(default=0)
    day_down_week_up_magnitude_std_tuesday = models.FloatField(default=0)

    day_down_week_down_odds_tuesday = models.FloatField(default=0)
    day_down_week_down_pct_tuesday = models.FloatField(default=0)
    day_down_week_down_pct_mean_tuesday = models.FloatField(default=0)
    day_down_week_down_pct_std_tuesday = models.FloatField(default=0)
    day_down_week_down_magnitude_tuesday = models.FloatField(default=0)
    day_down_week_down_magnitude_mean_tuesday = models.FloatField(default=0)
    day_down_week_down_magnitude_std_tuesday = models.FloatField(default=0)

    # Today's change
    chg_today_count_up_wednesday = models.IntegerField(default=0)
    chg_today_count_down_wednesday = models.IntegerField(default=0)
    chg_today_magnitude_wednesday = models.FloatField(default=0)
    chg_today_magnitude_mean_wednesday = models.FloatField(default=0)
    chg_today_magnitude_std_wednesday = models.FloatField(default=0)
    chg_today_percent_wednesday = models.FloatField(default=0)
    chg_today_percent_mean_wednesday = models.FloatField(default=0)
    chg_today_percent_std_wednesday = models.FloatField(default=0)
    #Change from yesterday
    chg_from_yest_count_up_wednesday = models.IntegerField(default=0)
    chg_from_yest_count_down_wednesday = models.IntegerField(default=0)
    chg_from_yest_magnitude_wednesday = models.FloatField(default=0)
    chg_from_yest_magnitude_mean_wednesday = models.FloatField(default=0)
    chg_from_yest_magnitude_std_wednesday = models.FloatField(default=0)
    chg_from_yest_percent_wednesday = models.FloatField(default=0)
    chg_from_yest_percent_mean_wednesday = models.FloatField(default=0)
    chg_from_yest_percent_std_wednesday = models.FloatField(default=0)

    # Wacky Wednesday
    total_weeks_wednesday = models.IntegerField(default=0)
    day_up_week_up_odds_wednesday = models.FloatField(default=0)
    day_up_week_up_pct_wednesday = models.FloatField(default=0)
    day_up_week_up_pct_mean_wednesday = models.FloatField(default=0)
    day_up_week_up_pct_std_wednesday = models.FloatField(default=0)
    day_up_week_up_magnitude_wednesday = models.FloatField(default=0)
    day_up_week_up_magnitude_mean_wednesday = models.FloatField(default=0)
    day_up_week_up_magnitude_std_wednesday = models.FloatField(default=0)

    day_up_week_down_odds_wednesday = models.FloatField(default=0)
    day_up_week_down_pct_wednesday = models.FloatField(default=0)
    day_up_week_down_pct_mean_wednesday = models.FloatField(default=0)
    day_up_week_down_pct_std_wednesday = models.FloatField(default=0)
    day_up_week_down_magnitude_wednesday = models.FloatField(default=0)
    day_up_week_down_magnitude_mean_wednesday = models.FloatField(default=0)
    day_up_week_down_magnitude_std_wednesday = models.FloatField(default=0)

    day_down_week_up_odds_wednesday = models.FloatField(default=0)
    day_down_week_up_pct_wednesday = models.FloatField(default=0)
    day_down_week_up_pct_mean_wednesday = models.FloatField(default=0)
    day_down_week_up_pct_std_wednesday = models.FloatField(default=0)
    day_down_week_up_magnitude_wednesday = models.FloatField(default=0)
    day_down_week_up_magnitude_mean_wednesday = models.FloatField(default=0)
    day_down_week_up_magnitude_std_wednesday = models.FloatField(default=0)

    day_down_week_down_odds_wednesday = models.FloatField(default=0)
    day_down_week_down_pct_wednesday = models.FloatField(default=0)
    day_down_week_down_pct_mean_wednesday = models.FloatField(default=0)
    day_down_week_down_pct_std_wednesday = models.FloatField(default=0)
    day_down_week_down_magnitude_wednesday = models.FloatField(default=0)
    day_down_week_down_magnitude_mean_wednesday = models.FloatField(default=0)
    day_down_week_down_magnitude_std_wednesday = models.FloatField(default=0)

    # Thirsty thursday
    chg_today_count_up_thursday = models.IntegerField(default=0)
    chg_today_count_down_thursday = models.IntegerField(default=0)
    chg_today_magnitude_thursday = models.FloatField(default=0)
    chg_today_magnitude_mean_thursday = models.FloatField(default=0)
    chg_today_magnitude_std_thursday = models.FloatField(default=0)
    chg_today_percent_thursday = models.FloatField(default=0)
    chg_today_percent_mean_thursday = models.FloatField(default=0)
    chg_today_percent_std_thursday = models.FloatField(default=0)
    #Change from yesterday
    chg_from_yest_count_up_thursday = models.IntegerField(default=0)
    chg_from_yest_count_down_thursday = models.IntegerField(default=0)
    chg_from_yest_magnitude_thursday = models.FloatField(default=0)
    chg_from_yest_magnitude_mean_thursday = models.FloatField(default=0)
    chg_from_yest_magnitude_std_thursday = models.FloatField(default=0)
    chg_from_yest_percent_thursday = models.FloatField(default=0)
    chg_from_yest_percent_mean_thursday = models.FloatField(default=0)
    chg_from_yest_percent_std_thursday = models.FloatField(default=0)

    # Week performance
    total_weeks_thursday = models.IntegerField(default=0)
    day_up_week_up_odds_thursday = models.FloatField(default=0)
    day_up_week_up_pct_thursday = models.FloatField(default=0)
    day_up_week_up_pct_mean_thursday = models.FloatField(default=0)
    day_up_week_up_pct_std_thursday = models.FloatField(default=0)
    day_up_week_up_magnitude_thursday = models.FloatField(default=0)
    day_up_week_up_magnitude_mean_thursday = models.FloatField(default=0)
    day_up_week_up_magnitude_std_thursday = models.FloatField(default=0)

    day_up_week_down_odds_thursday = models.FloatField(default=0)
    day_up_week_down_pct_thursday = models.FloatField(default=0)
    day_up_week_down_pct_mean_thursday = models.FloatField(default=0)
    day_up_week_down_pct_std_thursday = models.FloatField(default=0)
    day_up_week_down_magnitude_thursday = models.FloatField(default=0)
    day_up_week_down_magnitude_mean_thursday = models.FloatField(default=0)
    day_up_week_down_magnitude_std_thursday = models.FloatField(default=0)

    day_down_week_up_odds_thursday = models.FloatField(default=0)
    day_down_week_up_pct_thursday = models.FloatField(default=0)
    day_down_week_up_pct_mean_thursday = models.FloatField(default=0)
    day_down_week_up_pct_std_thursday = models.FloatField(default=0)
    day_down_week_up_magnitude_thursday = models.FloatField(default=0)
    day_down_week_up_magnitude_mean_thursday = models.FloatField(default=0)
    day_down_week_up_magnitude_std_thursday = models.FloatField(default=0)

    day_down_week_down_odds_thursday = models.FloatField(default=0)
    day_down_week_down_pct_thursday = models.FloatField(default=0)
    day_down_week_down_pct_mean_thursday = models.FloatField(default=0)
    day_down_week_down_pct_std_thursday = models.FloatField(default=0)
    day_down_week_down_magnitude_thursday = models.FloatField(default=0)
    day_down_week_down_magnitude_mean_thursday = models.FloatField(default=0)
    day_down_week_down_magnitude_std_thursday = models.FloatField(default=0)

    # Friday
    chg_today_count_up_friday = models.IntegerField(default=0)
    chg_today_count_down_friday = models.IntegerField(default=0)
    chg_today_magnitude_friday = models.FloatField(default=0)
    chg_today_magnitude_mean_friday = models.FloatField(default=0)
    chg_today_magnitude_std_friday = models.FloatField(default=0)
    chg_today_percent_friday = models.FloatField(default=0)
    chg_today_percent_mean_friday = models.FloatField(default=0)
    chg_today_percent_std_friday = models.FloatField(default=0)
    #Change from yesterday
    chg_from_yest_count_up_friday = models.IntegerField(default=0)
    chg_from_yest_count_down_friday = models.IntegerField(default=0)
    chg_from_yest_magnitude_friday = models.FloatField(default=0)
    chg_from_yest_magnitude_mean_friday = models.FloatField(default=0)
    chg_from_yest_magnitude_std_friday = models.FloatField(default=0)
    chg_from_yest_percent_friday = models.FloatField(default=0)
    chg_from_yest_percent_mean_friday = models.FloatField(default=0)
    chg_from_yest_percent_std_friday = models.FloatField(default=0)

    # Week performance
    total_weeks_friday = models.IntegerField(default=0)
    day_up_week_up_odds_friday = models.FloatField(default=0)
    day_up_week_up_pct_friday = models.FloatField(default=0)
    day_up_week_up_pct_mean_friday = models.FloatField(default=0)
    day_up_week_up_pct_std_friday = models.FloatField(default=0)
    day_up_week_up_magnitude_friday = models.FloatField(default=0)
    day_up_week_up_magnitude_mean_friday = models.FloatField(default=0)
    day_up_week_up_magnitude_std_friday = models.FloatField(default=0)

    day_up_week_down_odds_friday = models.FloatField(default=0)
    day_up_week_down_pct_friday = models.FloatField(default=0)
    day_up_week_down_pct_mean_friday = models.FloatField(default=0)
    day_up_week_down_pct_std_friday = models.FloatField(default=0)
    day_up_week_down_magnitude_friday = models.FloatField(default=0)
    day_up_week_down_magnitude_mean_friday = models.FloatField(default=0)
    day_up_week_down_magnitude_std_friday = models.FloatField(default=0)

    day_down_week_up_odds_friday = models.FloatField(default=0)
    day_down_week_up_pct_friday = models.FloatField(default=0)
    day_down_week_up_pct_mean_friday = models.FloatField(default=0)
    day_down_week_up_pct_std_friday = models.FloatField(default=0)
    day_down_week_up_magnitude_friday = models.FloatField(default=0)
    day_down_week_up_magnitude_mean_friday = models.FloatField(default=0)
    day_down_week_up_magnitude_std_friday = models.FloatField(default=0)

    day_down_week_down_odds_friday = models.FloatField(default=0)
    day_down_week_down_pct_friday = models.FloatField(default=0)
    day_down_week_down_pct_mean_friday = models.FloatField(default=0)
    day_down_week_down_pct_std_friday = models.FloatField(default=0)
    day_down_week_down_magnitude_friday = models.FloatField(default=0)
    day_down_week_down_magnitude_mean_friday = models.FloatField(default=0)
    day_down_week_down_magnitude_std_friday = models.FloatField(default=0)






