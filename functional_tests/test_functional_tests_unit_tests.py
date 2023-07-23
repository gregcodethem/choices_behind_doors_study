# These tests are to test the methods in the BaseTest work correctly

from django.contrib.auth.models import User

from selenium import webdriver

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


class FunctionalTestUnitTests(BaseTest):


    # Override setUp to pass without executing the setup in BaseTest
    def setUp(self):
        self.browser = webdriver.Firefox()

    def test_user_creation(self):
        """
        Test to see if a user is being created properly
        """


        # Check users already in the database:
        print([user.username for user in User.objects.all()])

        # Create a user using the method you want to test
        self.create_user(user_identifier="John", size="three_by_three")

        # Try to retrieve the created user from the database
        try:
            created_user = User.objects.get(username="johndoe")
            print(f"User {created_user.username} was successfully created!")
        except User.DoesNotExist:
            self.fail("User was not created")