from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from portfolios.models import Portfolio, Tag
from users.models import Profile  # Adjust if Profile is located elsewhere

class TagModelTest(TestCase):
    def test_create_tag(self):
        tag = Tag.objects.create(name="Tech")
        self.assertEqual(str(tag), "Tech")
        self.assertIsNotNone(tag.id)
        self.assertIsNotNone(tag.created_at)

class PortfolioModelTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(email="ebineezer_macintosh@gmail.com", 
                                        password="test123", 
                                        username="em123")
        
        self.profile = Profile.objects.get(user=self.user)

    def test_create_portfolio(self):
        portfolio = Portfolio.objects.create(
            owner=self.profile,
            name="My Portfolio",
            description="A test portfolio",
            portfolio_type=Portfolio.GROWTH_INVESTING
        )
        self.assertEqual(str(portfolio), "My Portfolio")
        self.assertEqual(portfolio.owner, self.profile)
        self.assertEqual(portfolio.portfolio_type, Portfolio.GROWTH_INVESTING)
        self.assertIsNotNone(portfolio.created_at)
        self.assertIsNotNone(portfolio.updated_at)

    def test_add_tags_to_portfolio(self):
        portfolio = Portfolio.objects.create(
            owner=self.profile,
            name="Tagged Portfolio",
            portfolio_type=Portfolio.SWING_TRADE
        )
        tag1 = Tag.objects.create(name="Finance")
        tag2 = Tag.objects.create(name="Energy")

        portfolio.tags.add(tag1, tag2)
        self.assertEqual(portfolio.tags.count(), 2)
        self.assertIn(tag1, portfolio.tags.all())
        self.assertIn(tag2, portfolio.tags.all())
