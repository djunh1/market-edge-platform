import uuid
from os import path

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from users.models import CustomUser, Profile
from portfolios.models import Portfolio, Tag
from portfolios.forms import PortfolioForm


def portfolios_url():
    return reverse('portfolios')

def portfolio_url(pk):
    return reverse('portfolio', args=(pk,))

def create_portfolio_url():
    return reverse('create-portfolio')

def update_portfolio_url(pk):
    return reverse('update-portfolio', args=(pk,))

def delete_portfolio_url(pk):
    return reverse('delete-portfolio', args=(pk,))

PORTFOLIO_TYPE = 'Swing trade, short term'

class TestPortfolioViews(TestCase):

    def setUp(self):
        """Set up test data for all test methods"""
        self.client = Client()
        
        User = get_user_model()
        self.user1 = CustomUser.objects.create_user(
            username='earl_newcastle',
            email='earl_newcastle@test.com',
            password='testpass123'
        )
        self.user2 = CustomUser.objects.create_user(
            username='earl_halifax',
            email='earl_halifax@test.com',
            password='testpass123'
        )
        
        # Create profiles (assuming they're created automatically or manually)
        self.profile1, _ = Profile.objects.get_or_create(user=self.user1)
        self.profile2, _ = Profile.objects.get_or_create(user=self.user2)
        
        # Create test portfolios
        self.portfolio1 = Portfolio.objects.create(
            description="Test description 1",
            owner=self.profile1
        )
        self.portfolio2 = Portfolio.objects.create(
            description="Test description 2",
            owner=self.profile2
        )
        
        # Create test tags
        self.tag1 = Tag.objects.create(name="technology")
        self.tag2 = Tag.objects.create(name="django")
        
        # Add tags to portfolio
        self.portfolio1.tags.add(self.tag1, self.tag2)

    def test_portfolios_view_requires_login_GET_failure(self) -> None:
        """Test that portfolios view requires authentication"""
        response = self.client.get(portfolios_url())
        self.assertEqual(response.status_code, 302)

    def test_portfolios_view_authenticated_user_GET_success(self) -> None:
        '''
        Tests that the portfolios page returns all portfolios
        '''
        self.client.login(username='earl_newcastle@test.com', password='testpass123')
    
        response = self.client.get(portfolios_url())

        portfolios = Portfolio.objects.all().order_by('id')  # Ensure consistent ordering
        expected_portfolios = [self.portfolio1, self.portfolio2]

        self.assertQuerySetEqual(
            portfolios,
            expected_portfolios,
            transform=lambda x: x,  # Don't transform, compare objects directly
            ordered=False
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['portfolios']), 2)

    def test_portfolio_detail_view_requires_login_GET_failure(self) -> None:
        '''
        Verify that the user is logged in before viewing the details of a portfolio
        '''
        url = portfolio_url(self.portfolio1.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_portfolio_detail_view_authenticated_user(self):
        """Test portfolio detail view with authenticated user"""
        self.client.login(email='earl_newcastle@test.com', password='testpass123')
        response = self.client.get(portfolio_url(self.portfolio1.id))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['portfolio'], self.portfolio1)

    def test_portfolio_detail_view_nonexistent_portfolio(self):
        """Test portfolio detail view with non-existent portfolio ID"""
        self.client.login(email='earl_newcastle@test.com', password='testpass123')
        with self.assertRaises(Portfolio.DoesNotExist):
            response = self.client.get(portfolio_url(uuid.uuid4()))
            self.assertEqual(response.status_code, 404)

    def test_create_portfolio_view_get_requires_login_GET_failure(self) -> None:
        """Test that create portfolio GET view requires authentication"""
        response = self.client.get(create_portfolio_url())
        self.assertEqual(response.status_code, 302)

    def test_create_portfolio_view_get_authenticated_user_GET_success(self):
        """Test create portfolio GET view with authenticated user"""
        self.client.login(email='earl_newcastle@test.com', password='testpass123')
        response = self.client.get(create_portfolio_url())
        
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], PortfolioForm)

    def test_create_portfolio_view_valid_data_POST_success(self) -> None:
        """Test create portfolio POST view with valid data"""
        self.client.login(email='earl_newcastle@test.com', password='testpass123')

        initial_count = Portfolio.objects.count()
        
        portfolio_data = {
            'name': 'six_nations_portfolio',
            'description': 'New test description',
            'portfolio_type': 'Swing trade, short term',
            'newtags': 'technology,crypto,new_tag'
        }
        
        response = self.client.post(create_portfolio_url(), data=portfolio_data)

        self.assertEqual(Portfolio.objects.count(), initial_count + 1)
        
        # Should redirect to account page after successful creation
        self.assertRedirects(response, reverse('account'))
        
        # Check that portfolio was created
        new_portfolio = Portfolio.objects.get(name="six_nations_portfolio")


        self.assertEqual(new_portfolio.owner, self.profile1)
        self.assertEqual(new_portfolio.description, 'New test description')
        
        # # Check that tags were created and associated
        self.assertTrue(new_portfolio.tags.filter(name='technology').exists())
        self.assertTrue(new_portfolio.tags.filter(name='crypto').exists())
        self.assertTrue(new_portfolio.tags.filter(name='new_tag').exists())

    def test_create_portfolio_view_invalid_data_POST_success(self) -> None:
        """Test create portfolio POST view with invalid data"""
        self.client.login(email='earl_newcastle@test.com', password='testpass123')
        
        # Missing required title field
        portfolio_data = {
            'description': 'Test description without title',
            'newtags': 'python'
        }
        
        response = self.client.post(create_portfolio_url(), data=portfolio_data)
        form = PortfolioForm(data=portfolio_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(response.status_code, 200)
        

    def test_update_portfolio_view_requires_login_GET_failure(self) -> None:
        """Test that update portfolio GET view requires authentication"""
        response = self.client.get(update_portfolio_url(self.portfolio1.id))
        self.assertEqual(response.status_code, 302)

    def test_update_portfolio_view_authenticated_owner_GET_succes(self) -> None:
        """Test update portfolio GET view with authenticated owner"""
        self.client.login(email='earl_newcastle@test.com', password='testpass123')
        response = self.client.get(update_portfolio_url(self.portfolio1.id))
    
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], PortfolioForm)
        self.assertEqual(response.context['portfolio'], self.portfolio1)

    def test_update_portfolio_view_non_owner_GET_failure(self) -> None:
        """Test update portfolio GET view with non-owner user"""
        self.client.login(email='earl_halifax@test.com', password='testpass123')
        with self.assertRaises(Portfolio.DoesNotExist):
            response = self.client.get(update_portfolio_url(self.portfolio1.id))

    def test_update_portfolio_view_valid_data_POST_success(self) -> None:
        """Test update portfolio POST view with valid data"""
        self.client.login(email='earl_newcastle@test.com', password='testpass123')
        
        updated_data = {
            'name': 'Updated Portfolio Title',
            'description': 'Updated description',
            'portfolio_type': 'Long term value investing',
            'newtags': 'semis,garbage'
        }
        
        response = self.client.post(
            update_portfolio_url(self.portfolio1.id),
            data=updated_data
        )
        
        self.assertEqual(response.status_code, 302)
        
        # Check that portfolio was updated
        updated_portfolio = Portfolio.objects.get(id=self.portfolio1.id)
        self.assertEqual(updated_portfolio.name, 'Updated Portfolio Title')
        self.assertEqual(updated_portfolio.portfolio_type, 'Long term value investing')
        self.assertEqual(updated_portfolio.description, 'Updated description')
        
        # Check that new tags were added
        self.assertTrue(updated_portfolio.tags.filter(name='semis').exists())
        self.assertTrue(updated_portfolio.tags.filter(name='garbage').exists())

    def test_update_portfolio_view_invalid_data_POST_sucess(self) -> None:
        """Test update portfolio POST view with invalid data"""
        self.client.login(email='earl_newcastle@test.com', password='testpass123')
        
        # Empty title should be invalid
        invalid_data = {
            'name': '',
            'description': 'Updated description',
            'newtags': 'tag1,tag2'
        }
        
        response = self.client.post(
            update_portfolio_url(self.portfolio1.id),
            data=invalid_data
        )
        
        # Should not redirect and should show form with errors
        self.assertEqual(response.status_code, 200)
        form = PortfolioForm(data=invalid_data)
        self.assertFalse(form.is_valid())

    def test_delete_portfolio_view_get_requires_login_GET_failure(self) -> None:
        """Test that delete portfolio GET view requires authentication"""
        response = self.client.get(delete_portfolio_url(self.portfolio1.id))
        self.assertEqual(response.status_code, 302)

    def test_delete_portfolio_view_get_authenticated_user_GET_success(self) -> None:
        """Test delete portfolio GET view with authenticated user"""
        self.client.login(email='earl_newcastle@test.com', password='testpass123')
        response = self.client.get(delete_portfolio_url(self.portfolio1.id))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object'], self.portfolio1)

    def test_delete_portfolio_view_post_authenticated_user_POST_failure(self) -> None:
        """Test delete portfolio POST view with authenticated user"""
        self.client.login(email='earl_newcastle@test.com', password='testpass123')
        
        # Verify portfolio exists before deletion
        self.assertTrue(Portfolio.objects.filter(id=self.portfolio1.id).exists())
        
        response = self.client.post(delete_portfolio_url(self.portfolio1.id))
        
        # Should redirect to account page after successful deletion
        self.assertRedirects(response, reverse('account'))
        
        # Verify portfolio was deleted
        self.assertFalse(Portfolio.objects.filter(id=self.portfolio1.id).exists())

    def test_delete_portfolio_view_nonexistent_portfolio_POSt_failure(self) -> None:
        """Test delete portfolio view with non-existent portfolio ID"""
        self.client.login(email='earl_newcastle@test.com', password='testpass123')
        with self.assertRaises(Portfolio.DoesNotExist):
            response = self.client.post(delete_portfolio_url(uuid.uuid4()))

    def test_create_portfolio_with_empty_newtags_POST_sucess(self) -> None:
        """Test create portfolio with empty newtags field"""
        self.client.login(email='earl_newcastle@test.com', password='testpass123')
        
        portfolio_data = {
            'name': 'Portfolio Without Tags',
            'description': 'Description without tags',
            'portfolio_type': 'Long term value investing',
            'newtags': ''
        }
        
        response = self.client.post(create_portfolio_url(), data=portfolio_data)
        
        # Should still work and redirect
        self.assertEqual(response.status_code, 302)
        
        # Portfolio should be created
        new_portfolio = Portfolio.objects.get(name='Portfolio Without Tags')
        self.assertEqual(new_portfolio.owner, self.profile1)

    def test_update_portfolio_with_comma_separated_tags_POST_success(self) -> None:
        """Test update portfolio with comma-separated tags"""
        self.client.login(email='earl_newcastle@test.com', password='testpass123')
        
        updated_data = {
            'name': 'Portfolio Without Tags',
            'description': 'Description without tags',
            'portfolio_type': 'Long term value investing',
            'newtags': 'tag1,tag2,tag3'
        }
        
        response = self.client.post(
            update_portfolio_url(self.portfolio1.id),
            data=updated_data
        )
        
        self.assertEqual(response.status_code, 302)
        
        # Check that tags were properly parsed and created
        updated_portfolio = Portfolio.objects.get(id=self.portfolio1.id)
        self.assertTrue(updated_portfolio.tags.filter(name='tag1').exists())
        self.assertTrue(updated_portfolio.tags.filter(name='tag2').exists())
        self.assertTrue(updated_portfolio.tags.filter(name='tag3').exists())

    # Todo Add when stocks are implemented
    # def test_stock_view_requires_login(self)-> None:
    #     """Test that stock view requires authentication"""
    #     response = self.client.get(reverse('stock', kwargs={'pk': 1}))
    #     self.assertRedirects(response, '/login/?next=' + reverse('stock', kwargs={'pk': 1}))

    # def test_stock_view_authenticated_user(self):
    #     """Test stock view with authenticated user"""
    #     self.client.login(email='earl_newcastle@test.com', password='testpass123')
    #     response = self.client.get(reverse('stock', kwargs={'pk': 1}))
        
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, 'Caesar')




