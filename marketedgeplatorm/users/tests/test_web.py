import datetime
from os import path

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from users.models import CustomUser, Profile
from portfolios.models import Portfolio, Tag
from users.forms import ProfileForm

import sys
import uuid

PORTFOLIO_TYPE = 'Swing trade, short term'


def signup_url():
    return reverse('register')

def logout_url():
    return reverse('logout')

def user_profile_url(pk):
    return reverse('user-profile', args=(pk,))

def profiles_url():
    return reverse('profiles')

def account_url():
    return reverse('account')

def edit_account_url():
    return reverse('edit-account')

class TestUserViews(TestCase):


    def today():
        return datetime.date.today()
    
    def setUp(self):
        User = get_user_model()
        dan_Zanger = CustomUser.objects.create_user(username="danZanger", email='dan_Zanger@test.com', password='subprime_is_contained')
        dan_Zanger.save()
        self.dans_profile = Profile.objects.get(user=dan_Zanger)
        
        # dans_profile.save()

        self.tag1 = Tag.objects.create(name='Semis')
        self.tag2 = Tag.objects.create(name='Tech')
        self.tag3 = Tag.objects.create(name='Customer Discretionary')

        self.portfolio_1 = Portfolio.objects.create(owner=self.dans_profile,
                                    portfolio_type=PORTFOLIO_TYPE,
                                    name="My Long term value portfolio",
                                    description="A normal description")

        self.portfolio_1.save()

        self.portfolio_1.tags.add(self.tag1)

        self.portfolio_2 = Portfolio.objects.create(owner=self.dans_profile,
                                    portfolio_type=PORTFOLIO_TYPE,
                                    name="My Long term value portfolio",
                                    description="A normal description")

        self.portfolio_2.save()

        # Second test user
        pradeep_bonde = CustomUser.objects.create_user(username="stockbee", email='stockbee@test.com', password='always_think_3_days_ahead')
        pradeep_bonde.save()
        self.pradeeps_profile = Profile.objects.get(user=pradeep_bonde)

        self.stock_bee_portfolio = Portfolio.objects.create(owner=self.pradeeps_profile,
                                    portfolio_type=PORTFOLIO_TYPE,
                                    name="My Long term value portfolio",
                                    description="A normal description")

        self.stock_bee_portfolio.save()

    def test_successful_login(self) -> None:
        '''
        Login normally
        '''
        logged_in = self.client.login(email='dan_Zanger@test.com', password='subprime_is_contained')
        self.assertTrue(logged_in)
        

    def test_failed_login_invalid_credentials(self) -> None:
        '''
        Login with incorrect credentials
        '''
        logged_in = self.client.login(username='dan_Zanger@test.com', password='not_my_pass')
        self.assertFalse(logged_in) # Assert that the login was unsuccessful

        # You can also check for redirects or specific error messages
        response = self.client.post('/accounts/login/', {'email': 'dan_Zanger@test.com', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 404)
        

    def test_user_logout_endpoint_GET_success(self)-> None:
        '''
        logs out and redirect.  Not rocket science
        '''
        url = logout_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/users/login/', status_code=302, 
        target_status_code=200, fetch_redirect_response=True)


    def test_user_profile_endpoint_GET_success(self)-> None:
        '''
        Fetch a profile - Requires login
        '''
        login = self.client.login(username='dan_Zanger@test.com', password='subprime_is_contained')

        self.assertTrue(login)

        dan_zanger = CustomUser.objects.all().first()

        url = user_profile_url(self.dans_profile.id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/user-profile.html")
        self.assertEqual(response.context['user'], dan_zanger)
        self.assertEqual(response.context['profile'], dan_zanger.profile)


    def test_user_profile_endpoint_GET_success_others_profile(self) -> None:
        '''
        Fetch a profile - Verify it is their profile
        '''
        self.client.login(username='dan_Zanger@test.com', password='subprime_is_contained')

        url = user_profile_url(self.pradeeps_profile.id)
        response = self.client.get(url)
 
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['profile'], self.pradeeps_profile)

    def test_user_profile_endpoint_GET_fail(self):
        '''
        Fetch a profile - User is not logged in
        '''

        url = user_profile_url(self.dans_profile.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_user_profiles_endpoint_GET_fail(self) -> None:
        '''
        User can not fetch profiles if they are not logged in
        '''
        url = profiles_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_user_profiles_endpoint_GET_success(self) -> None:
        '''
        User can  fetch profiles if they are  logged in
        '''
        login = self.client.login(username='dan_Zanger@test.com', password='subprime_is_contained')
        url = profiles_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


    def test_redirect_if_not_logged_in_GET_redirect(self) -> None:
        '''
        Redirects if not logged in
        '''

        url = account_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_view_url_exists_for_logged_in_user_GET_success(self) -> None:
        self.client.login(username='dan_Zanger@test.com', password='subprime_is_contained')
        url = account_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_correct_template_used(self) -> None:
        self.client.login(username='dan_Zanger@test.com', password='subprime_is_contained')
        url = account_url()
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'users/account.html')

    def test_account_belongs_to_user_GET_success(self) -> None:
        '''
        Verify that the profile belongs to first user, and their portfolios are loaded
        '''
        self.client.login(username='dan_Zanger@test.com', password='subprime_is_contained')
        url = account_url()
        response = self.client.get(url)
        self.assertEqual(response.context['profile'], self.dans_profile)
        self.assertIn(self.portfolio_1, response.context['portfolios'])
        self.assertIn(self.portfolio_2, response.context['portfolios'])
        self.assertNotIn(self.stock_bee_portfolio, response.context['portfolios'])

    def test_if_not_logged_in_edit_account_GET_failure(self) -> None:
        '''
        Can not get into an account if not logged in
        '''
        url = edit_account_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_edit_account_view_get(self) -> None:
        '''
        Verify that user can edit their account with the correct form
        '''
        logged_in = self.client.login(username='dan_Zanger@test.com', password='subprime_is_contained')
        self.assertTrue(logged_in)

        url = edit_account_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile_form.html')
        self.assertIsInstance(response.context['form'], ProfileForm)

    def test_edit_account_valid_data_POST_success(self) -> None:
        '''
        Tests valid form update from a POST request
        '''
        self.client.login(username='dan_Zanger@test.com', password='subprime_is_contained')
        data = {
            'username': 'dan_zanger_2',
            'bio': 'Updated bio',
        }

        response = self.client.post(edit_account_url(), data)
        self.assertRedirects(response, reverse('account'))
        self.dans_profile.refresh_from_db()
        self.assertEqual(self.dans_profile.username, 'dan_zanger_2')
        self.assertEqual(self.dans_profile.bio, 'Updated bio')

    def test_edit_account_post_invalid_data(self) -> None:
        '''
        Can not update the email
        '''
        self.client.login(username='testuser', password='testpass')
        data = {'email': 'another_persons_email@test.com'}  
        response = self.client.post(edit_account_url(), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.dans_profile.email, 'dan_Zanger@test.com')
        self.assertNotEqual(self.dans_profile.email, 'another_persons_email@test.com')





