"""Test module for login app"""
from django.test import TestCase
from django.contrib.auth import authenticate
from django.utils.crypto import get_random_string
from django.db.utils import IntegrityError
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from .models import CustomUser
# Create your tests here.

class CustomUserTestCase(TestCase):
    """ Class for testing user model and functions """

    def setup(self):
        """ Set up of testing environments """
        self.token1 = get_random_string(length=32)
        self.token2 = get_random_string(length=32)
        u1 = CustomUser.objects.create_user("email@email.com", "password1")
        u2 = CustomUser.objects.create_user("email1@email.com", "password1")

        u1.verify_token = self.token1
        u1.name = "Carlos"
        u1.save()

        u2.verify_token = self.token2
        u2.name = "Alex"
        u2.save()

    def cleanup(self):
        """ Remove all test objects """
        CustomUser.objects.all().delete()

    def test_verify_user(self):
        """ Testing user.verify() """
        self.setup()
        temp_user = CustomUser.objects.get(name="Carlos")

        self.assertEqual(temp_user.verify(self.token2), False)
        self.assertAlmostEqual(temp_user.verified, False)
        self.assertEqual(temp_user.verify(self.token1), True)
        self.assertAlmostEqual(temp_user.verified, True)

    def test_user_creation(self):
        """ Test that can create new users, check that no user can be created
        twice """
        self.setup()
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                user = CustomUser.objects.create_user("email@email.com",
                    "password1")
                user.save()

        user = CustomUser.objects.create_user("email2@email.com", "password1")
        user.save()
        self.assertIsInstance(user, CustomUser)
        self.assertEqual(CustomUser.objects.count(), 3)

    def test_user_authenticate(self):
        """
        Test that user can be authenticated with correct password and fails
        if wrong password
        """
        self.setup()
        self.assertIsNone(authenticate(username="email@email.com",
            password="hamandcheese"))
        self.assertIsInstance(authenticate(username="email@email.com",
            password="password1"), CustomUser)

    def test_user_deletion(self):
        """ Test that users are deleted, it should also be expanded to check
        that when a user is deleted the projects owned by that user are
        also deleted """
        self.setup()
        CustomUser.objects.get(email="email@email.com").delete()
        self.assertEqual(CustomUser.objects.count(), 1)
        with self.assertRaises(ObjectDoesNotExist):
            with transaction.atomic():
                CustomUser.objects.get(email="email@email.com")
