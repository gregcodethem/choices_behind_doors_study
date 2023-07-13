from unittest import skip

from doorgame.models import Trial, Profile
from django.contrib.auth.models import User

from .base import BaseTest


class TrialNumberTest(BaseTest):

    def test_home_page_gives_trial_number(self):
        self.login_temp()
        response = self.client.get('/memory_game_initial_turn', follow=True)

        html = response.content.decode('utf8')
        self.assertIn('Trial number 1', html)

    @skip
    def test_home_page_gives_trial_number_two_for_second_trial(self):
        # I don't think this test is relevant anymore
        # as it is run on memory_game_initial_turn
        # but it shouldn't be run if it's not the initial turn

        # I should change this test, if memory_game_inital_turn
        # has already been run, then the view should redirect to something else


        user_test = User.objects.create_user(
            'george',
            '',
            'somethingpassword')
        user_test.save()
        profile = user_test.profile
        profile.hard_or_easy_dots = 'easy'
        profile.save()
        first_trial = Trial()
        first_trial.user = user_test
        first_trial.number_of_trial = 1
        first_trial.save()

        self.client.login(username='george', password='somethingpassword')
        response = self.client.get('/memory_game_initial_turn', follow=True)

        html = response.content.decode('utf8')
        self.assertIn('Trial number 2', html)

    def test_trial_number_created_when_memory_game_accessed(self):
        self.login_temp()
        user = User.objects.get(username='temporary')
        response = self.client.get(
            '/memory_game_initial_turn',
            )
        trials_list = Trial.objects.all() # <----refactor out!!!!!
        trial_created = Trial.objects.last()
        number_of_trial = trial_created.number_of_trial

        self.assertEqual(len(trials_list),1)

