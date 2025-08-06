import uuid
from django.test import TestCase, RequestFactory

from django.core.paginator import Paginator
from django.db import models
from unittest.mock import Mock

from users.models import CustomUser, Profile
from portfolios.models import Portfolio, Tag
from portfolios.utils import searchPortfolios, paginatePortfolios



class SearchPortfoliosTestCase(TestCase):
    def setUp(self):
        """Set up test data"""
        self.factory = RequestFactory()
        
        # Create test users and profiles
        # self.user1 = User.objects.create_user(username='testuser1', email='test1@example.com')
        # self.user2 = User.objects.create_user(username='investor2', email='test2@example.com')
        
        # self.profile1 = Profile.objects.create(user=self.user1, username='testuser1')
        # self.profile2 = Profile.objects.create(user=self.user2, username='investor2')
        
        # Create test tags
        self.tag1 = Tag.objects.create(name='Technology')
        self.tag2 = Tag.objects.create(name='Healthcare')
        self.tag3 = Tag.objects.create(name='Finance')


        self.factory = RequestFactory()
        
        # Create test users and profiles
        self.user1 =CustomUser.objects.create_user(username="testuser1", 
                                                    email='test1@example.com', 
                                                    password='fortNessesity')
        self.user2 = CustomUser.objects.create_user(username="investor2", 
                                                    email='test2@example.com', 
                                                    password='printingpress')
        
        self.profile1 = Profile.objects.get(user=self.user1)
        self.profile2 = Profile.objects.get(user=self.user2)

 
        # Create test portfolios
        self.portfolio1 = Portfolio.objects.create(
            name='Tech Growth Portfolio',
            description='A portfolio focused on technology growth stocks',
            owner=self.profile1,
            portfolio_type=Portfolio.GROWTH_INVESTING
        )
        self.portfolio1.tags.add(self.tag1)
        
        self.portfolio2 = Portfolio.objects.create(
            name='Healthcare Value',
            description='Long-term healthcare investments',
            owner=self.profile2,
            portfolio_type=Portfolio.LONG_TERM_VALUE
        )
        self.portfolio2.tags.add(self.tag2)
        
        self.portfolio3 = Portfolio.objects.create(
            name='Swing Trading Portfolio',
            description='Short-term trading strategies',
            owner=self.profile1,
            portfolio_type=Portfolio.SWING_TRADE
        )
        self.portfolio3.tags.add(self.tag3)

    def test_search_portfolios_no_query(self):
        """Test searchPortfolios with no search query"""
        request = self.factory.get('/')
        portfolios, search_query = searchPortfolios(request)
        
        self.assertEqual(search_query, '')
        self.assertEqual(portfolios.count(), 3)
        
    def test_search_portfolios_by_name(self):
        """Test searching portfolios by name"""
        request = self.factory.get('/?search_query=Tech')
        portfolios, search_query = searchPortfolios(request)
        
        self.assertEqual(search_query, 'Tech')
        self.assertEqual(portfolios.count(), 1)
        self.assertIn(self.portfolio1, portfolios)
        
    def test_search_portfolios_by_description(self):
        """Test searching portfolios by description"""
        request = self.factory.get('/?search_query=healthcare')
        portfolios, search_query = searchPortfolios(request)
        
        self.assertEqual(search_query, 'healthcare')
        self.assertEqual(portfolios.count(), 1)
        self.assertIn(self.portfolio2, portfolios)
        
    def test_search_portfolios_by_owner_username(self):
        """Test searching portfolios by owner username"""
        request = self.factory.get('/?search_query=investor2')
        portfolios, search_query = searchPortfolios(request)
        
        self.assertEqual(search_query, 'investor2')
        self.assertEqual(portfolios.count(), 1)
        self.assertIn(self.portfolio2, portfolios)
        
    def test_search_portfolios_by_portfolio_type(self):
        """Test searching portfolios by portfolio type"""
        request = self.factory.get('/?search_query=Growth')
        portfolios, search_query = searchPortfolios(request)
        
        self.assertEqual(search_query, 'Growth')
        self.assertEqual(portfolios.count(), 1)
        self.assertIn(self.portfolio1, portfolios)
        
    def test_search_portfolios_by_tag(self):
        """Test searching portfolios by tags"""
        request = self.factory.get('/?search_query=Technology')
        portfolios, search_query = searchPortfolios(request)
        
        self.assertEqual(search_query, 'Technology')
        self.assertEqual(portfolios.count(), 1)
        self.assertIn(self.portfolio1, portfolios)
        
    def test_search_portfolios_case_insensitive(self):
        """Test that search is case insensitive"""
        request = self.factory.get('/?search_query=TECH')
        portfolios, search_query = searchPortfolios(request)
        
        self.assertEqual(search_query, 'TECH')
        self.assertEqual(portfolios.count(), 1)
        self.assertIn(self.portfolio1, portfolios)
        
    def test_search_portfolios_multiple_results(self):
        """Test search query that matches multiple portfolios"""
        request = self.factory.get('/?search_query=Portfolio')
        portfolios, search_query = searchPortfolios(request)
        
        self.assertEqual(search_query, 'Portfolio')
        self.assertEqual(portfolios.count(), 2)  # Tech Growth Portfolio and Swing Trading Portfolio
        
    def test_search_portfolios_no_results(self):
        """Test search query with no matching results"""
        request = self.factory.get('/?search_query=nonexistent')
        portfolios, search_query = searchPortfolios(request)
        
        self.assertEqual(search_query, 'nonexistent')
        self.assertEqual(portfolios.count(), 0)

    def test_search_portfolios_distinct_results(self):
        """Test that search returns distinct results when portfolio matches multiple criteria"""
        # Create a portfolio that matches both name and description for same query
        portfolio = Portfolio.objects.create(
            name='Crypto Crypto',
            description='Cryptocurrency investments in crypto market',
            owner=self.profile1
        )
        
        request = self.factory.get('/?search_query=crypto')
        portfolios, search_query = searchPortfolios(request)
        
        # Should return only one instance of the portfolio despite matching multiple fields
        portfolio_ids = [p.id for p in portfolios]
        self.assertEqual(len(portfolio_ids), len(set(portfolio_ids)))


class PaginatePortfoliosTestCase(TestCase):
    def setUp(self):
        """Set up test data"""
        self.factory = RequestFactory()
        
        # Create test user and profile
        self.user =CustomUser.objects.create_user(username="testuser", 
                                                    email='test@example.com', 
                                                    password='fortNessesity')
        self.profile = Profile.objects.get(user=self.user)
        
        # Create 15 test portfolios for pagination testing
        self.portfolios = []
        for i in range(15):
            portfolio = Portfolio.objects.create(
                name=f'Portfolio {i+1}',
                description=f'Description for portfolio {i+1}',
                owner=self.profile
            )
            self.portfolios.append(portfolio)

    def test_paginate_portfolios_first_page(self):
        """Test pagination for first page"""
        request = self.factory.get('/?page=1')
        portfolios_qs = Portfolio.objects.all()
        
        custom_range, paginated_portfolios = paginatePortfolios(request, portfolios_qs, 5)
        
        self.assertEqual(len(paginated_portfolios), 5)
        self.assertEqual(paginated_portfolios.number, 1)
        self.assertEqual(list(custom_range), [1, 2, 3])  # Should show pages 1-3 (1+5, but capped at total pages)

    def test_paginate_portfolios_middle_page(self):
        """Test pagination for middle page"""
        request = self.factory.get('/?page=2')
        portfolios_qs = Portfolio.objects.all()
        
        custom_range, paginated_portfolios = paginatePortfolios(request, portfolios_qs, 5)
        
        self.assertEqual(len(paginated_portfolios), 5)
        self.assertEqual(paginated_portfolios.number, 2)
        self.assertEqual(list(custom_range), [1, 2, 3])  # For 15 items with 5 per page = 3 total pages

    def test_paginate_portfolios_last_page(self):
        """Test pagination for last page"""
        request = self.factory.get('/?page=3')
        portfolios_qs = Portfolio.objects.all()
        
        custom_range, paginated_portfolios = paginatePortfolios(request, portfolios_qs, 5)
        
        self.assertEqual(len(paginated_portfolios), 5)  # 15 total, 10 on first 2 pages, 5 on last
        self.assertEqual(paginated_portfolios.number, 3)
        self.assertEqual(list(custom_range), [1, 2, 3])

    def test_paginate_portfolios_no_page_parameter(self):
        """Test pagination when no page parameter is provided"""
        request = self.factory.get('/')
        portfolios_qs = Portfolio.objects.all()
        
        custom_range, paginated_portfolios = paginatePortfolios(request, portfolios_qs, 5)
        
        self.assertEqual(paginated_portfolios.number, 1)  # Should default to page 1
        self.assertEqual(len(paginated_portfolios), 5)

    def test_paginate_portfolios_invalid_page_number(self):
        """Test pagination with invalid page number (non-integer)"""
        request = self.factory.get('/?page=invalid')
        portfolios_qs = Portfolio.objects.all()
        
        custom_range, paginated_portfolios = paginatePortfolios(request, portfolios_qs, 5)
        
        self.assertEqual(paginated_portfolios.number, 1)  # Should default to page 1
        self.assertEqual(len(paginated_portfolios), 5)

    def test_paginate_portfolios_page_out_of_range(self):
        """Test pagination with page number out of range"""
        request = self.factory.get('/?page=999')
        portfolios_qs = Portfolio.objects.all()
        
        custom_range, paginated_portfolios = paginatePortfolios(request, portfolios_qs, 5)
        
        self.assertEqual(paginated_portfolios.number, 3)  # Should go to last page (3)
        self.assertEqual(len(paginated_portfolios), 5)

    def test_paginate_portfolios_custom_range_large_dataset(self):
        """Test custom range with large dataset"""
        # Create more portfolios for a larger dataset
        for i in range(85):  # Add 85 more (total 100)
            Portfolio.objects.create(
                name=f'Extra Portfolio {i+1}',
                description=f'Extra description {i+1}',
                owner=self.profile
            )
        
        request = self.factory.get('/?page=10')  # Middle page of 20 total pages (100 portfolios, 5 per page)
        portfolios_qs = Portfolio.objects.all()
        
        custom_range, paginated_portfolios = paginatePortfolios(request, portfolios_qs, 5)
        
        self.assertEqual(paginated_portfolios.number, 10)
        # Custom range should be [6, 7, 8, 9, 10, 11, 12, 13, 14] (page-4 to page+4)
        expected_range = list(range(6, 15))
        self.assertEqual(list(custom_range), expected_range)

    def test_paginate_portfolios_custom_range_beginning(self):
        """Test custom range at the beginning when leftIndex would be < 1"""
        request = self.factory.get('/?page=1')
        portfolios_qs = Portfolio.objects.all()
        
        custom_range, paginated_portfolios = paginatePortfolios(request, portfolios_qs, 5)
        
        # leftIndex should be adjusted to 1, rightIndex should be page + 5 = 6, but capped at num_pages + 1 = 4
        expected_range = list(range(1, 4))  # [1, 2, 3]
        self.assertEqual(list(custom_range), expected_range)

    def test_paginate_portfolios_different_results_per_page(self):
        """Test pagination with different number of results per page"""
        request = self.factory.get('/?page=1')
        portfolios_qs = Portfolio.objects.all()
        
        custom_range, paginated_portfolios = paginatePortfolios(request, portfolios_qs, 10)
        
        self.assertEqual(len(paginated_portfolios), 10)
        self.assertEqual(paginated_portfolios.number, 1)
        # With 15 portfolios and 10 per page, we have 2 pages
        expected_range = list(range(1, 3))  # [1, 2]
        self.assertEqual(list(custom_range), expected_range)

    def test_paginate_portfolios_empty_queryset(self):
        """Test pagination with empty queryset"""
        request = self.factory.get('/?page=1')
        empty_qs = Portfolio.objects.none()
        
        custom_range, paginated_portfolios = paginatePortfolios(request, empty_qs, 5)
        
        self.assertEqual(len(paginated_portfolios), 0)
        self.assertEqual(paginated_portfolios.number, 1)
        self.assertEqual(list(custom_range), [1])  # Single page even with no results