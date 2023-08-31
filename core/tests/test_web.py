import datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import Client, TestCase
from django.urls import reverse
from core.models.models_study import Study

from core.models.models_message import Message
from users.models import CustomUser
from weekdayStudy.models import WeekdayStudy

STUDY_DESCRIPTION = 'Sample Study for url testing'
STUDY_MESSAGE = 'A sample study message'
STUDY_TYPE = 'weekday_study'

def study_url(pk):
    return reverse('study', args=(pk,))

class TestUserViews(TestCase):

    '''
    TODO eventually this entire application will be locked down and a user will need to be logged in.
    '''

    def today():
        return datetime.date.today()

    def setUp(self):

        study_date = datetime.date.today()
        User = get_user_model()
        alan_greenspan = CustomUser.objects.create_user(name="alan_greenspan", email='alan_greenspan@test.com', password='irrational_exuberence')

        alan_greenspan.save()


        first_study = WeekdayStudy.objects.create(study_creator=alan_greenspan,
                                    study_type=STUDY_TYPE,
                                    ticker="IONQ",
                                    study_date_end=study_date,
                                    description = STUDY_DESCRIPTION)

        first_study.save()

        second_study = WeekdayStudy.objects.create(study_creator=alan_greenspan,
                                    study_type=STUDY_TYPE,
                                    ticker="CVNA",
                                    study_date_end=study_date,
                                    description = STUDY_DESCRIPTION)

        second_study.save()

        first_message = Message.objects.create(
            user=alan_greenspan,
            study=first_study,
            body=STUDY_MESSAGE)

        second_message = Message.objects.create(
            user=alan_greenspan,
            study=second_study,
            body=STUDY_MESSAGE)

        first_message.save()
        second_message.save()

    # HOME PAGE (get) basic search via the navbar.
    def test_core_home_endpoint_GET_success_no_objects(self):
        '''
        No search - should return all objects in the DB
        '''
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "base/home.html")
        self.assertEqual(response.context['study_count'], 2)
        self.assertEqual(response.context['studies'].count(), 2)
        self.assertEqual(response.context['study_messages'].count(), 2)

    def test_core_home_endpoint_GET_success_multiple_objects(self):
        '''
        Search for a study with specific ticker
        '''
        payload = {
            'q': 'IONQ'
        }

        url = reverse('home')

        response = self.client.get(url, payload)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "base/home.html")
        self.assertEqual(response.context['study_count'], 1)
        self.assertEqual(response.context['studies'].count(), 1)
        self.assertEqual(response.context['study_messages'].count(), 1)

    def test_core_home_endpoint_GET_failure_bad_query(self):
        '''
        Nothing is returned if the search is malformed, but still
        will be a 200 response from the home page
        '''
        payload = {
            'q': 'garbage'
        }

        url = reverse('home')

        response = self.client.get(url, payload)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "base/home.html")
        self.assertEqual(response.context['study_count'], 0)
        self.assertEqual(response.context['studies'].count(), 0)
        self.assertEqual(response.context['study_messages'].count(), 0)

    # INDIVIDUAL STUDY (get, post)
    def test_core_study_endpoint_GET_success(self):
        '''
        Fetch a single study - this study only has one message
        '''
        primary_uuid = WeekdayStudy.objects.all().first().id

        url = study_url(primary_uuid)

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['study_creator'].email, 'alan_greenspan@test.com')
        self.assertEqual(response.context['study'].id, primary_uuid)
        self.assertEqual(response.context['study_messages'].count(), 1)

    def test_core_study_endpoint_GET_fail(self):
        '''
        Attempt to fetch a study with a bad ID - backend throws validation error
        '''
        primary_uuid = 'fakeuuid'

        url = study_url(primary_uuid)
        with self.assertRaises(ValidationError):
            response = self.client.get(url)

    def test_core_study_endpoint_POST_failure(self):
        '''
        Only a logged in user can create a message
        '''
        payload = {
            'body': 'Any Federal Reserve bank may make application to the local Federal Reserve agent for such amount of the Federal Reserve notes hereinbefore provided for as it may require.'
            }
        primary_uuid = WeekdayStudy.objects.all().first().id
        url = study_url(primary_uuid)
        with self.assertRaises(ValueError):
            response = self.client.post(url, payload)

    def test_core_study_endpoint_POST_success(self):
        '''
        Only a logged in user can create a message, redirects to the study page
        '''
        primary_uuid = WeekdayStudy.objects.all().first().id

        login = self.client.login(username='alan_greenspan@test.com', password='irrational_exuberence')

        self.assertTrue(login)

        payload = {
            'body': 'Federal reserve notes, to be issued at the discretion of the Board of Governors of the Federal Reserve System for the purpose of making advances to Federal reserve banks through the Federal reserve agents as hereinafter set forth and for no other purpose, are hereby authorized'
            }
        url = study_url(primary_uuid)
        response = self.client.post(url, payload)

        self.assertEqual(response.status_code, 302)
        msg  = Message.objects.first() #first message is newest
        self.assertEqual(msg.body, "Federal reserve notes, to be issued at the discretion of the Board of Governors of the Federal Reserve System for the purpose of making advances to Federal reserve banks through the Federal reserve agents as hereinafter set forth and for no other purpose, are hereby authorized")

        self.client.logout()

