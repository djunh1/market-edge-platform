import datetime
import unittest

from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Study, StudyType
from users.models import CustomUser
from weekdayStudy.models import WeekdayStudy

STOCK_TICKER = 'NVDA'
STUDY_DESCRIPTION = 'Weekday study'

class WeekdayStudyTestCase(TestCase):

    def today():
        return datetime.date.today()

    def setUp(self):
        study_date = datetime.date.today()
        User = get_user_model()
        user = User.objects.create_user(email="hat-tricks@unassisted.com",
                                        password="t3h-23rv1c3-D3sk")

        study_type = StudyType.objects.create(status='weekday_study')
        WeekdayStudy.objects.create(study_creator=user,
                                    study_type=study_type,
                                    ticker=STOCK_TICKER,
                                    study_date_end=study_date,
                                    description = STUDY_DESCRIPTION,
                                    chg_today_count_up_monday=25,
                                    chg_today_count_down_monday=22,
                                    chg_today_magnitude_monday=2.2,
                                    chg_today_percent_monday=1.23,
                                    chg_from_yest_count_up_monday=26,
                                    chg_from_yest_count_down_monday=21,
                                    chg_from_yest_magnitude_monday =0.5,
                                    chg_from_yest_percent_monday =1.1,
                                    total_weeks_monday=47,
                                    day_up_week_up_pct_monday=38.3,
                                    day_up_week_up_magnitude_monday=22,
                                    day_up_week_down_pct_monday=14.9,
                                    day_up_week_down_magnitude_monday=8.7,
                                    day_down_week_up_pct_monday=27.7,
                                    day_down_week_up_magnitude_monday=17.9,
                                    day_down_week_down_pct_monday=19.1,
                                    day_down_week_down_magnitude_monday=15
                                    )

    def test_populating_weekday_study(self):
        # Discuss this as a model before making the migrations...
        nvda_study = WeekdayStudy.objects.all().first()
        self.assertEqual(nvda_study.chg_today_count_up_monday, 25)

