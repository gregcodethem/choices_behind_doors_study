from django.test import TestCase

from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from doorgame.models import Profile


class BaseTest(TestCase):
    def setUp(self):
        # Create user
        User = get_user_model()
        user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')

        # Get or create the profile associated with the user
        profile, created = Profile.objects.get_or_create(user=user)

        # Update the profile fields
        profile.hard_or_easy_dots = "easy"
        # profile.low_medium_or_high_dots_setting = "medium"  # Uncomment if needed
        profile.prelim_completed = False
        profile.memory_game_list_created = False
        profile.regret_forwards = True

        # Save the updated profile
        profile.save()


    def login_temp(self):
        User = get_user_model()
        self.client.login(username='temporary', password='temporary')

