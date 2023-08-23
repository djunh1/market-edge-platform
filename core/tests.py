import datetime
import unittest

from django.contrib.auth import get_user_model
from django.test import TestCase

from .models.models_study import Study, StudyType
from users.models import CustomUser
from weekdayStudy.models import WeekdayStudy

STOCK_TICKER = 'NVDA'
STUDY_DESCRIPTION = 'A cool study'

class StudyTestCase(TestCase):

    def today():
        return datetime.date.today()

    def setUp(self):
        study_date = datetime.date.today()
        User = get_user_model()
        user = User.objects.create_user(email="hat-tricks@unassisted.com", password="t3h-23rv1c3-D3sk")

        study_type = StudyType.objects.create(status='weekday_study')
        WeekdayStudy.objects.create(study_creator=user,
                                    study_type=study_type,
                                    ticker=STOCK_TICKER,
                                    study_date_end=study_date,
                                    description = STUDY_DESCRIPTION)

    def test_create_default_study_setup(self):
        study_type = StudyType.objects.create(status='weekday_study')
        TEST_STRING ='[{study_type}]-{ticker}__({study_date_end})'.format(study_type=study_type.__str__(), ticker=STOCK_TICKER, study_date_end=datetime.date.today())

        nvda_study = WeekdayStudy.objects.all().first()
        user_nvda_study = CustomUser.objects.all().first()

        self.assertEqual(nvda_study.__str__(), TEST_STRING)
        self.assertEqual(nvda_study.description, STUDY_DESCRIPTION)
        self.assertEqual(nvda_study.study_creator, user_nvda_study)

        User = get_user_model()
        another_user = User.objects.create_user(email="pleaseProvide@theNEEDFUL.com", password="isThisAP1IfICantRestoreADevDB?")

        # Check to make sure some other rando can't make a study
        self.assertNotEqual(nvda_study.study_creator, another_user)
        self.assertAlmostEqual(nvda_study.study_type.__str__(), study_type.__str__())

    def test_create_default_study_type(self):
        study_type = StudyType.objects.create()
        self.assertEqual(study_type.status.__str__(), 'weekday_study')

    def test_another_study_type(self):
        study_type = StudyType.objects.create(status='fundamentals_study')
        self.assertEqual(study_type.status.__str__(), 'fundamentals_study')

    def test_study_create_fail(self):
        '''
        Do this later
        '''
        FAKE_USER_STUDY_TYPE ='random_study'

        study_type = StudyType.objects.create(status=FAKE_USER_STUDY_TYPE)
        User = get_user_model()

        user = User.objects.create_user(email="mr-derp@unassisted.com", password="t3h-23rv1c3-D3sk")


if __name__ == '__main__':
    unittest.main()


