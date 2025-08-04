from django.contrib.auth import get_user_model
from users.models import Profile
from django.test import TestCase

from django.conf import settings
from unittest.mock import patch
import os

class UsersManagersTests(TestCase):

    def test_create_user(self) -> None:
        '''
        Create normal user, is not staff or super user of application
        '''
        User = get_user_model()
        user = User.objects.create_user(email="normal@user.com", 
                                        password="foo", 
                                        username="test_user")
        self.assertEqual(user.email, "normal@user.com")
        self.assertEqual(user.username, "test_user")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email="")
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="foo")

    def test_create_superuser(self) -> None:
        '''
        Testing the creation of a superuser
        '''
        User = get_user_model()
        admin_user = User.objects.create_superuser(email="super@user.com", password="foo")
        self.assertEqual(admin_user.email, "super@user.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="super@user.com", password="foo", is_superuser=False)

    @patch('django.core.files.storage.FileSystemStorage._save', return_value='images/default.jpg')
    def test_create_profile(self, mock_save) -> None:
        '''
        Profile is automatically created when a user is created
        '''
        User = get_user_model()
        profile_user = User.objects.create_user(email="profile@user.com", 
                                        password="test", 
                                        username="profile_user")
        
        profile = Profile.objects.get(user=profile_user)

   
        self.assertEqual(profile.email, "profile@user.com")
        self.assertEqual(profile.username, "profile_user")
        self.assertIsNone(profile.bio)
        self.assertIsNotNone(profile.profile_image)
        self.assertTrue(profile.profile_image.url.endswith('/user-default.png'))


    @patch('django.core.files.storage.FileSystemStorage._save', return_value='images/default.jpg')
    def test_update_profile(self, mock_save) -> None:
        '''
        Profile is automatically created when a user is created
        '''
        User = get_user_model()
        profile_user = User.objects.create_user(email="profile@user.com", 
                                        password="test", 
                                        username="profile_user")
        
        profile = Profile.objects.get(user=profile_user)
        profile.bio = "my new bio"
        profile.username = "new_username"

        profile.save()
   
        self.assertEqual(profile.email, "profile@user.com")
        self.assertEqual(profile.username, "new_username")
        self.assertIsNotNone(profile.bio)
        self.assertEqual(profile.bio, "my new bio")
        self.assertIsNotNone(profile.profile_image)
        self.assertTrue(profile.profile_image.url.endswith('/user-default.png'))
    
    @patch('django.core.files.storage.FileSystemStorage._save', return_value='images/default.jpg')
    def test_delete_user(self, mock_save) -> None:
        '''
        Verifies profile is deleted when the user is deleted
        '''
        User = get_user_model()
        profile_user = User.objects.create_user(email="profile@user.com", 
                                        password="test", 
                                        username="profile_user")
        
        profile = Profile.objects.get(user=profile_user)

        user_id = profile_user.id
        profile_id = profile.id
        profile_user.delete()

        with self.assertRaises(User.DoesNotExist):
                User.objects.get(id=user_id)

        with self.assertRaises(Profile.DoesNotExist):
                Profile.objects.get(id=profile_id)