import datetime
from os import path

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from core.models.models_message import Message
from users.models import CustomUser
from weekdayStudy.models import WeekdayStudy

STUDY_DESCRIPTION = 'Testing the User views here'
STUDY_MESSAGE = 'More study messages from the bernak'
STUDY_TYPE = 'weekday_study'

def signup_url():
    return reverse('register')

def logout_url():
    return reverse('logout')

def user_profile_url(pk):
    return reverse('user-profile', args=(pk,))

class TestUserViews(TestCase):

    '''
    TODO eventually this entire application will be locked down and a user will need to be logged in.
    '''

    def today():
        return datetime.date.today()

    def setUp(self):
        study_date = datetime.date.today()
        User = get_user_model()
        ben_bernake = CustomUser.objects.create_user(name="ben_bernake", email='ben_bernake@test.com', password='subprime_is_contained')

        ben_bernake.save()
        first_study = WeekdayStudy.objects.create(study_creator=ben_bernake,
                                    study_type=STUDY_TYPE,
                                    ticker="TSLA",
                                    study_date_end=study_date,
                                    description = STUDY_DESCRIPTION)

        first_study.save()

        second_study = WeekdayStudy.objects.create(study_creator=ben_bernake,
                                    study_type=STUDY_TYPE,
                                    ticker="NIO",
                                    study_date_end=study_date,
                                    description = STUDY_DESCRIPTION)

        second_study.save()

        first_message = Message.objects.create(
            user=ben_bernake,
            study=first_study,
            body=STUDY_MESSAGE)

        second_message = Message.objects.create(
            user=ben_bernake,
            study=second_study,
            body=STUDY_MESSAGE)

        first_message.save()
        second_message.save()

    def test_user_logout_endpoint_GET_success(self):
        '''
        logs out and redirect.  Not rocket science
        '''
        url = logout_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        #self.assertTemplateUsed(response, "base/home.html")

    def test_user_profile_endpoint_GET_success(self):
        '''
        Fetch a profile - for now this does not require a log in
        '''
        ben_bernak = CustomUser.objects.all().first()
        user_pk = ben_bernak.id

        url = user_profile_url(user_pk)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profile.html")
        self.assertEqual(response.context['user'], ben_bernak)
        self.assertEqual(response.context['studies'].count(), 2)
        self.assertEqual(response.context['study_messages'].count(),2)

    def test_user_profile_endpoint_GET_bad_key(self):
        '''
        Use a bad key, error thrown
        '''

        user_pk = 'not_a_key'
        url = user_profile_url(user_pk)

        with self.assertRaises(ValueError):
            response = self.client.get(url)

    def test_user_update_endpoint_GET_not_logged_in(self):
        '''
        redirects to login page if not logged in
        '''

        url = reverse('update-user')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        # self.assertRedirects(response, reverse('login'), status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

    def test_user_update_endpoint_GET_logged_in(self):
        '''
        Will render the update user's profile if logged in
        '''

        login = self.client.login(username='ben_bernake@test.com', password='subprime_is_contained')

        self.assertTrue(login)

        url = reverse('update-user')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "update-user.html")


    def test_user_update_endpoint_POST_not_logged_in(self):
        '''
        Can not post to the user profile if they aren't logged in.
        '''
        url = reverse('update-user')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)

    def test_user_update_endpoint_POST_logged_in(self):
        '''
        Will render the update user's profile and image
        '''

        login = self.client.login(username='ben_bernake@test.com', password='subprime_is_contained')

        self.assertTrue(login)

        filepath = path.abspath(path.join(path.dirname(__file__), "files", "bernak.png"))

        with open(filepath, "rb") as fp:
            response = self.client.post(reverse('update-user'),
                              {  'name': "Bill__McAdoo",
                                 'email' : 'newEmail@test.com',
                                 'avatar': fp
                              })

        self.assertEqual(response.status_code, 302)

        ben_bernak_upgrade = CustomUser.objects.all().first()
        self.assertEqual(ben_bernak_upgrade.name, "Bill__McAdoo")
        self.assertEqual(ben_bernak_upgrade.email, "newEmail@test.com")







