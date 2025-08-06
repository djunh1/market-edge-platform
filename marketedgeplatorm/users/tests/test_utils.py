from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.core.paginator import Page


from users.models import CustomUser, Profile # Replace 'myapp' with your actual app name
from users.utils import searchProfiles, paginateProfiles  # Replace 'myapp' with your actual app name

from django.urls import reverse

class SearchProfilesTestCase(TestCase):
    def setUp(self):
        """Set up test data"""
        self.factory = RequestFactory()
        
        # Create test users and profiles
        self.user1 =CustomUser.objects.create_user(username="washington", 
                                                    email='user1@test.com', 
                                                    password='fortNessesity')
        self.user2 = CustomUser.objects.create_user(username="franklin", 
                                                    email='user2@test.com', 
                                                    password='printingpress')
        self.user3 = CustomUser.objects.create_user(username="braddock_manager", 
                                                    email='user3@test.com', 
                                                    password='timeToInvadeTheFrench')
        
        self.profile1 = Profile.objects.get(user=self.user1)
        self.profile2 = Profile.objects.get(user=self.user2)
        self.profile3 = Profile.objects.get(user=self.user3)

        # Update bios
        self.profile1.bio = "Its Christmas, lets cross the deleware river"
        self.profile1.save()
        self.profile2.bio = "delete me, I messed up"
        self.profile2.save()
        self.profile3.bio = "I am a manager"
        self.profile3.save()


    def test_search_profiles_no_query(self):
        """Test searchProfiles with no search query"""
        request = self.factory.get('/profiles/')
        
        profiles, search_query = searchProfiles(request)
        
        self.assertEqual(search_query, '')
        self.assertEqual(profiles.count(), 3)
        self.assertIn(self.profile1, profiles)
        self.assertIn(self.profile2, profiles)
        self.assertIn(self.profile3, profiles)

    def test_search_profiles_empty_query(self):
        """Test searchProfiles with empty search query"""
        request = self.factory.get('/profiles/?search_query=')
        
        profiles, search_query = searchProfiles(request)
        
        self.assertEqual(search_query, '')
        self.assertEqual(profiles.count(), 3)

    def test_search_profiles_username_match(self):
        """Test searchProfiles with username search"""
        request = self.factory.get('/profiles/?search_query=washington')
        
        profiles, search_query = searchProfiles(request)
        
        self.assertEqual(search_query, 'washington')
        self.assertEqual(profiles.count(), 1)
        self.assertIn(self.profile1, profiles)
        self.assertNotIn(self.profile2, profiles)
        self.assertNotIn(self.profile3, profiles)

    def test_search_profiles_bio_match(self):
        """Test searchProfiles with bio content search"""
        request = self.factory.get('/profiles/?search_query=deleware')
        
        profiles, search_query = searchProfiles(request)
        
        self.assertEqual(search_query, 'deleware')
        self.assertEqual(profiles.count(), 1)
        self.assertIn(self.profile1, profiles)

    def test_search_profiles_case_insensitive(self):
        """Test searchProfiles case insensitive search"""
        request = self.factory.get('/profiles/?search_query=DELEWARE')
        
        profiles, search_query = searchProfiles(request)
        
        self.assertEqual(search_query, 'DELEWARE')
        self.assertEqual(profiles.count(), 1)
        self.assertIn(self.profile1, profiles)

    def test_search_profiles_partial_match(self):
        """Test searchProfiles with partial string match"""
        request = self.factory.get('/profiles/?search_query=del')
        
        profiles, search_query = searchProfiles(request)
        
        self.assertEqual(search_query, 'del')
        self.assertEqual(profiles.count(), 2)  # 'delete' and 'deleware'
        self.assertIn(self.profile1, profiles)
        self.assertIn(self.profile2, profiles)

    def test_search_profiles_no_matches(self):
        """Test searchProfiles with query that matches nothing"""
        request = self.factory.get('/profiles/?search_query=nonexistent')
        
        profiles, search_query = searchProfiles(request)
        
        self.assertEqual(search_query, 'nonexistent')
        self.assertEqual(profiles.count(), 0)

    def test_search_profiles_multiple_matches(self):
        """Test searchProfiles with query matching multiple fields"""
        request = self.factory.get('/profiles/?search_query=manager')
        
        profiles, search_query = searchProfiles(request)
        
        self.assertEqual(search_query, 'manager')
        self.assertEqual(profiles.count(), 1)
        self.assertIn(self.profile3, profiles)


class PaginateProfilesTestCase(TestCase):
    def setUp(self):
        """Set up test data"""
        self.factory = RequestFactory()
        
        # Create multiple profiles for pagination testing
        self.profiles = []
        for i in range(15):
            user =CustomUser.objects.create_user(username="gw_{i}", 
                                                    email=f'user{i}@test.com', 
                                                    password=f'unassisted{i}')
            profile = Profile.objects.get(user=user)
            profile.username = f"gw_{i}"
            profile.bio = f'Bio for user {i}'
            profile.save()
            self.profiles.append(profile)


    def test_paginate_profiles_first_page(self):
        """Test pagination for first page"""
        profiles_queryset = Profile.objects.all()
        request = self.factory.get('/profiles/?page=1')
        
        custom_range, paginated_profiles = paginateProfiles(request, profiles_queryset, 5)
        
        self.assertIsInstance(paginated_profiles, Page)
        self.assertEqual(len(paginated_profiles), 5)
        self.assertEqual(paginated_profiles.number, 1)
        self.assertEqual(list(custom_range), [1, 2, 3])  # leftIndex=1, rightIndex=6, but capped at num_pages+1

    def test_paginate_profiles_middle_page(self):
        """Test pagination for middle page"""
        profiles_queryset = Profile.objects.all()
        request = self.factory.get('/profiles/?page=2')
        
        custom_range, paginated_profiles = paginateProfiles(request, profiles_queryset, 5)
        
        self.assertEqual(paginated_profiles.number, 2)
        self.assertEqual(len(paginated_profiles), 5)

    def test_paginate_profiles_last_page(self):
        """Test pagination for last page"""
        profiles_queryset = Profile.objects.all()
        request = self.factory.get('/profiles/?page=3')
        
        custom_range, paginated_profiles = paginateProfiles(request, profiles_queryset, 5)
        
        self.assertEqual(paginated_profiles.number, 3)
        self.assertEqual(len(paginated_profiles), 5)  # 15 profiles, 5 per page, last page has 5

    def test_paginate_profiles_no_page_parameter(self):
        """Test pagination when no page parameter is provided"""
        profiles_queryset = Profile.objects.all()
        request = self.factory.get('/profiles/')
        
        custom_range, paginated_profiles = paginateProfiles(request, profiles_queryset, 5)
        
        self.assertEqual(paginated_profiles.number, 1)  # Should default to page 1

    def test_paginate_profiles_invalid_page_number(self):
        """Test pagination with invalid page number (non-integer)"""
        profiles_queryset = Profile.objects.all()
        request = self.factory.get('/profiles/?page=invalid')
        
        custom_range, paginated_profiles = paginateProfiles(request, profiles_queryset, 5)
        
        self.assertEqual(paginated_profiles.number, 1)  # Should default to page 1

    def test_paginate_profiles_page_too_high(self):
        """Test pagination when page number exceeds available pages"""
        profiles_queryset = Profile.objects.all()
        request = self.factory.get('/profiles/?page=999')
        
        custom_range, paginated_profiles = paginateProfiles(request, profiles_queryset, 5)
        
        self.assertEqual(paginated_profiles.number, 3)  # Should go to last page (15 items / 5 per page = 3 pages)

    def test_paginate_profiles_custom_range_left_boundary(self):
        """Test custom range calculation at left boundary"""
        profiles_queryset = Profile.objects.all()
        request = self.factory.get('/profiles/?page=1')
        
        custom_range, paginated_profiles = paginateProfiles(request, profiles_queryset, 5)
        
        # leftIndex = (1 - 4) = -3, but should be capped at 1
        # rightIndex = (1 + 5) = 6, but we have 3 pages so should be capped at 4
        expected_range = range(1, 4)  # pages 1, 2, 3
        self.assertEqual(list(custom_range), list(expected_range))

    def test_paginate_profiles_custom_range_right_boundary(self):
        """Test custom range calculation at right boundary"""
        profiles_queryset = Profile.objects.all()
        request = self.factory.get('/profiles/?page=3')
        
        custom_range, paginated_profiles = paginateProfiles(request, profiles_queryset, 5)
        
        # leftIndex = (3 - 4) = -1, but should be capped at 1
        # rightIndex = (3 + 5) = 8, but we have 3 pages so should be capped at 4
        expected_range = range(1, 4)  # pages 1, 2, 3
        self.assertEqual(list(custom_range), list(expected_range))

    def test_paginate_profiles_different_results_per_page(self):
        """Test pagination with different number of results per page"""
        profiles_queryset = Profile.objects.all()
        request = self.factory.get('/profiles/?page=1')
        
        custom_range, paginated_profiles = paginateProfiles(request, profiles_queryset, 10)
        
        self.assertEqual(len(paginated_profiles), 10)
        self.assertEqual(paginated_profiles.paginator.num_pages, 2)  # 15 items / 10 per page = 2 pages

    def test_paginate_profiles_single_page(self):
        """Test pagination when all results fit on one page"""
        profiles_queryset = Profile.objects.all()
        request = self.factory.get('/profiles/?page=1')
        
        custom_range, paginated_profiles = paginateProfiles(request, profiles_queryset, 20)
        
        self.assertEqual(len(paginated_profiles), 15)  # All 15 profiles on one page
        self.assertEqual(paginated_profiles.paginator.num_pages, 1)
        self.assertEqual(list(custom_range), [1])

    def test_paginate_profiles_empty_queryset(self):
        """Test pagination with empty queryset"""
        empty_queryset = Profile.objects.none()
        request = self.factory.get('/profiles/?page=1')
        
        custom_range, paginated_profiles = paginateProfiles(request, empty_queryset, 5)
        
        self.assertEqual(len(paginated_profiles), 0)
        self.assertEqual(paginated_profiles.paginator.num_pages, 1)  # Paginator creates at least 1 page


class IntegrationTestCase(TestCase):
    """Integration tests combining both utility functions"""
    
    def setUp(self):
        """Set up test data"""
        self.factory = RequestFactory()
        
        # Create test profiles
        for i in range(10):
            user =CustomUser.objects.create_user(username="gw_{i}", 
                                                    email=f'user{i}@test.com', 
                                                    password=f'unassisted{i}')
            profile = Profile.objects.get(user=user)
            profile.username = f'developer{i}' if i < 5 else f'designer{i}',
            profile.bio = f'Bio for user {i}'
            profile.save()

    def test_search_and_paginate_integration(self):
        """Test using searchProfiles output with paginateProfiles"""
        # Search for developers
        search_request = self.factory.get('/profiles/?search_query=developer')
        profiles, search_query = searchProfiles(search_request)
        
        # Paginate the search results
        paginate_request = self.factory.get('/profiles/?page=1')
        custom_range, paginated_profiles = paginateProfiles(paginate_request, profiles, 3)
        
        self.assertEqual(search_query, 'developer')
        self.assertEqual(profiles.count(), 5)  # 5 developers
        self.assertEqual(len(paginated_profiles), 3)  # 3 per page
        self.assertEqual(paginated_profiles.paginator.num_pages, 2)  # 5 results / 3 per page = 2 pages