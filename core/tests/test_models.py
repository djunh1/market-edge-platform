import datetime
import unittest

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase

from core.models.models_study import Study
from core.models.models_message import Message

from users.models import CustomUser
from weekdayStudy.models import WeekdayStudy

from django.core.exceptions import ValidationError

STOCK_TICKER = 'NVDA'
STUDY_DESCRIPTION = 'A cool study'
STUDY_TYPE = 'weekday_study'

class TestModels(TestCase):

    def today():
        return datetime.date.today()

    def setUp(self):

        study_date = datetime.date.today()
        User = get_user_model()
        user = CustomUser.objects.create_user(email="bill-martin@test.com", password="t3h-23rv1c3-D3sk")


        WeekdayStudy.objects.create(study_creator=user,
                                    study_type=STUDY_TYPE,
                                    ticker=STOCK_TICKER,
                                    study_date_end=study_date,
                                    description = STUDY_DESCRIPTION)

    def test_create_default_study_setup(self):

        TEST_STRING ='[{study_type}]-{ticker}__({study_date_end})'.format(study_type=STUDY_TYPE, ticker=STOCK_TICKER, study_date_end=datetime.date.today())

        nvda_study = WeekdayStudy.objects.all().first()
        user_nvda_study = CustomUser.objects.all().first()

        self.assertEqual(nvda_study.__str__(), TEST_STRING)
        self.assertEqual(nvda_study.description, STUDY_DESCRIPTION)
        self.assertEqual(nvda_study.study_creator, user_nvda_study)

        User = get_user_model()
        another_user = User.objects.create_user(email="pleaseProvide@theNEEDFUL.com", password="isThisAP1IfICantRestoreADevDB?")

        # Check to make sure some other rando can't make a study
        self.assertNotEqual(nvda_study.study_creator, another_user)
        self.assertAlmostEqual(nvda_study.study_type.__str__(), STUDY_TYPE)
        self.assertEqual(nvda_study.message_set.all().count(),0)


    def test_study_create_fail(self):
        '''
        Verifies that you cant create a study without a User, the correct study type name and a ticker.
        '''
        FAKE_USER_STUDY_TYPE ='random_study'


        User = get_user_model()

        user = User.objects.create_user(email="ben-bernake@test.test", password="t3h-23rv1c3-D3sk")

        with self.assertRaises(ValidationError):
            study_bad_study_name = WeekdayStudy.objects.create(study_creator=user,
                                study_type=FAKE_USER_STUDY_TYPE,
                                ticker=STOCK_TICKER)
            study_bad_study_name.full_clean()

        with self.assertRaises(ValidationError):
            study_no_ticker = WeekdayStudy.objects.create(study_creator=user, study_type='weekday_study')
            study_no_ticker.full_clean()

        with self.assertRaises(ValidationError):
            study_no_user = WeekdayStudy.objects.create(
                                study_type=FAKE_USER_STUDY_TYPE,
                                ticker=STOCK_TICKER)
            study_no_user.full_clean()



    def test_study_has_messages(self):
        '''
        Verify that a study can have multiple messages from multiple users
        '''
        MESSAGE_BODY = "N MONDAY, October 21, 1907, the Na­tional Bank of Commerce of New York City announced its refusal to clear for theKnickerbocker Trust Company of the same city. The trust company had deposits amounting to $62,000,000."
        TRUNCATED = MESSAGE_BODY[0:50]
        user_bill_martin = CustomUser.objects.all().first()
        user_Marriner_Eccles = CustomUser.objects.create_user(email="marriner@test.com", password="t3h-23rv1c3-D3sk")
        nvda_study = WeekdayStudy.objects.all().first()
        first_message = Message.objects.create(
            user=user_bill_martin,
            study=nvda_study,
            body=MESSAGE_BODY)

        second_message = Message.objects.create(
            user=user_Marriner_Eccles,
            study=nvda_study,
            body=MESSAGE_BODY)

        self.assertEqual(nvda_study.message_set.all().count(),2)
        self.assertEqual(first_message.user, user_bill_martin)
        self.assertEqual(second_message.user, user_Marriner_Eccles)
        self.assertEqual(first_message.body, MESSAGE_BODY)

        self.assertEqual(str(first_message), TRUNCATED)

    def test_message_create_fail_no_study(self):
        '''
        Verifies that you cant create a message without a study
        '''
        user_bill_martin = CustomUser.objects.all().first()
        nvda_study = WeekdayStudy.objects.all().first()

        MESSAGE_BODY = 'A message in a study'

        with self.assertRaises(IntegrityError):
            second = Message.objects.create(
            user=user_bill_martin,
            body=MESSAGE_BODY)
            second.full_clean()

    def test_message_create_fail_no_user(self):
        '''
        Verifies that you cant create a message without a User
        '''
        user_bill_martin = CustomUser.objects.all().first()
        nvda_study = WeekdayStudy.objects.all().first()

        MESSAGE_BODY = 'A message in a study'

        with self.assertRaises(IntegrityError):
            first_message = Message.objects.create(
            study=nvda_study,
            body=MESSAGE_BODY)
            first_message.full_clean()
            first_message.delete()

    def test_message_create_fail_no_body(self):
        '''
        Verifies that you cant create a message without a Body
        '''
        user_bill_martin = CustomUser.objects.all().first()
        nvda_study = WeekdayStudy.objects.all().first()

        MESSAGE_BODY = None

        with self.assertRaises(IntegrityError):
            first_message = Message.objects.create(
            user=user_bill_martin,
            study=nvda_study,
            body=MESSAGE_BODY)
            first_message.full_clean()


if __name__ == '__main__':
    unittest.main()


