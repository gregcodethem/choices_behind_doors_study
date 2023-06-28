# These tests are to test the methods in the BaseTest work correctly

from django.contrib.auth.models import User

from .base import BaseTest


class FunctionalTestUnitTests(BaseTest):

    def test_user_created(self):
        # User should be created from SetUp method in base test

        # Retrieve the user from the database
        user = User.objects.get(username='johndoe')

        self.assertEqual(user.username, 'johndoe')

    def test_created_user_can_login(self):
        # Retrieve the user from the database
        user = User.objects.get(username='johndoe')

        # You can also check if you can authenticate the user
        self.assertTrue(self.client.login(username='johndoe', password='bigfisharetasty3'))
