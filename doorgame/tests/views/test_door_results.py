from unittest.mock import patch

from django.urls import resolve
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.test import override_settings

from doorgame.views import final_door_result_page
from doorgame.models import (
    Choice,
    Trial,
    Result,
)

from .test_door_result_one import DoorResultPageTest


class FinalDoorResultPageTest(DoorResultPageTest):

    def setUp(self):
        super().setUp()
        self.login_temp()
        self.user = User.objects.get(username='temporary')
        # An associated trial also needs to be created
        self.trial = Trial()
        self.trial.user = self.user
        self.trial.number_of_trial = 1
        self.trial.save()

        # The result of the door game, needs to be fed into
        # this view, so an instance of this needs to be created here
        self.result = Result()
        self.result.trial = self.trial
        self.result.door_number = 1
        self.result.save()

    def create_choice(self, door_number, first_or_second_choice):
        choice = Choice()
        choice.door_number = door_number
        choice.first_or_second_choice = first_or_second_choice
        choice.trial = self.trial
        choice.save()

    def test_final_door_result_url_resolves_to_final_door_page_view(self):
        found = resolve('/user/temporary/final-door-result')
        self.assertEqual(found.func, final_door_result_page)

    def test_outcome_of_doorgame_returns_correct_html(self):

        # create a choice for this trial,
        # this shows the door choice they've made
        self.create_choice(door_number=1,first_or_second_choice=1)
        self.create_choice(door_number=1,first_or_second_choice=2)

        response = self.client.get('/outcome_of_doorgame', follow=True)

        html = response.content.decode('utf8')
        self.assertIn('The result of your final door choice', html)


    def test_outcome_of_doorgame_returns_correct_template(self):


        # create a choice for this trial,
        # this shows the door choice they've made
        self.create_choice(door_number=1,first_or_second_choice=1)
        self.create_choice(door_number=1,first_or_second_choice=2)

        response = self.client.get('/outcome_of_doorgame', follow=True)

        self.assertTemplateUsed(response,'final_door_result.html')



    def test_final_door_result_url_redirects_to_regret_page(self):

        # create a choice for this trial,
        # this shows the door choice they've made
        self.create_choice(door_number=1,first_or_second_choice=1)
        self.create_choice(door_number=1,first_or_second_choice=2)

        response_client = self.client.get('/user/temporary/final-door-result', follow=True)
        self.assertTemplateUsed(response_client,'regret.html')

    @override_settings(TRIAL_LIMIT=5)
    def test_final_door_result_page_returns_box_grid_when_trial_limit_not_reached(self):

        # create a choice for this trial,
        # this shows the door choice they've made
        self.create_choice(door_number=1,first_or_second_choice=1)
        self.create_choice(door_number=1,first_or_second_choice=2)

        response_client = self.client.get('/user/temporary/final-door-result', follow=True)

        self.assertTemplateUsed(response_client,'mem_game_blank_base.html')


class ChooseFinalDoorTest(DoorResultPageTest):
    def test_choose_final_door_method_keeping_door_redirects(self):
        self.door_result_page_login_and_model_setup()

        response = self.client.post(
            '/choose_final_door',
            {'door_chosen':1}
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/user/temporary/final-door-result')

    def test_choose_final_door_method_keeping_door_saves_choice(self):
        self.door_result_page_login_and_model_setup(
            choose_door_url_to_be_called=False
        )

        response = self.client.post(
            '/choose_final_door',
            {'final_door_chosen': 1}
        )

        # extract model data here
        user = User.objects.get(username='temporary')
        trial = Trial.objects.filter(user=user).last()
        choice_existing_objects = Choice.objects.filter(trial=trial)
        final_door_choice = choice_existing_objects.last()
        choice_first_or_second = final_door_choice.first_or_second_choice
        choice_door_chosen = final_door_choice.door_number

        self.assertEqual(len(choice_existing_objects),2)
        self.assertEqual(choice_first_or_second, 2)
        self.assertEqual(choice_door_chosen, 1)

    def test_choose_final_door_method_changing_door_redirects(self):
        # set up, this choses the first door as one by default
        self.door_result_page_login_and_model_setup(
            choose_door_url_to_be_called=False
        )

        # as we're just recording if they stick or switch
        # it dosen't matter which door they change to, only that they change
        response_change_to_two = self.client.post(
            '/choose_final_door',
            {'door_chosen':2}
        )

        self.assertEqual(response_change_to_two.status_code, 302)
        self.assertEqual(response_change_to_two['location'], '/user/temporary/final-door-result')

        response_change_to_three = self.client.post(
            '/choose_final_door',
            {'door_chosen': 3}
        )

        self.assertEqual(response_change_to_three.status_code, 302)
        self.assertEqual(response_change_to_three['location'], '/user/temporary/final-door-result')

    def test_choose_final_door_method_changing_door_saves_choice(self):
        self.door_result_page_login_and_model_setup(
            choose_door_url_to_be_called=False
        )

        response = self.client.post(
            '/choose_final_door',
            {'final_door_chosen': 2}
        )

        # extract model data here
        user = User.objects.get(username='temporary')
        trial = Trial.objects.filter(user=user).last()
        choice_existing_objects = Choice.objects.filter(trial=trial)
        final_door_choice = choice_existing_objects.last()
        choice_first_or_second = final_door_choice.first_or_second_choice
        choice_door_chosen = final_door_choice.door_number

        self.assertEqual(len(choice_existing_objects),2)
        self.assertEqual(choice_first_or_second, 2)
        self.assertEqual(choice_door_chosen, 2)
