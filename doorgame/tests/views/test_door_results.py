from unittest.mock import patch

from django.urls import resolve
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from doorgame.views import final_door_result_page
from doorgame.models import (
    Choice,
    Trial,
    Result,
)
from .base import BaseTest
from .test_door_result_one import DoorResultPageTest


class FinalDoorResultPageTest(DoorResultPageTest):

    def test_final_door_result_url_resolves_to_final_door_page_view(self):
        found = resolve('/user/temporary/final-door-result')
        self.assertEqual(found.func, final_door_result_page)

    def test_outcome_of_doorgame_returns_correct_html(self):
        self.login_temp()
        user = User.objects.get(username='temporary')
        # An associated trial also needs to be created
        # as this is usually created by the view:
        # memory_game_initial_turn
        trial = Trial()
        trial.user = user
        trial.number_of_trial = 1
        trial.save()

        # The result of the door game, needs to be fed into
        # this view, so an instance of this needs to be created here
        result = Result()
        result.trial = trial
        result.door_number = 1
        result.save()

        # create a choice for this trial,
        # this shows the door choice they've made
        choice_one = Choice()
        choice_one.door_number = 1
        choice_one.first_or_second_choice = 1
        choice_one.trial = trial
        choice_one.save()

        choice_two = Choice()
        choice_two.door_number = 1
        choice_two.first_or_second_choice = 2
        choice_two.trial = trial
        choice_two.save()

        response = self.client.get('/outcome_of_doorgame', follow=True)

        html = response.content.decode('utf8')
        self.assertIn('The result of your final door choice', html)



    def test_outcome_of_doorgame_returns_correct_template(self):
        self.login_temp()
        user = User.objects.get(username='temporary')
        # An associated trial also needs to be created
        # as this is usually created by the view:
        # memory_game_initial_turn
        trial = Trial()
        trial.user = user
        trial.number_of_trial = 1
        trial.save()

        # The result of the door game, needs to be fed into
        # this view, so an instance of this needs to be created here
        result = Result()
        result.trial = trial
        result.door_number = 1
        result.save()

        # create a choice for this trial,
        # this shows the door choice they've made
        choice_one = Choice()
        choice_one.door_number = 1
        choice_one.first_or_second_choice = 1
        choice_one.trial = trial
        choice_one.save()

        choice_two = Choice()
        choice_two.door_number = 1
        choice_two.first_or_second_choice = 2
        choice_two.trial = trial
        choice_two.save()

        response = self.client.get('/outcome_of_doorgame', follow=True)

        self.assertTemplateUsed(response,'final_door_result.html')



    def test_final_door_result_url_redirects_to_regret_page(self):

        self.login_temp()
        user = User.objects.get(username='temporary')
        # An associated trial also needs to be created
        # as this is usually created by the view:
        # memory_game_initial_turn
        trial = Trial()
        trial.user = user
        trial.number_of_trial = 1
        trial.save()

        # The result of the door game, needs to be fed into
        # this view, so an instance of this needs to be created here
        result = Result()
        result.trial = trial
        result.door_number = 1
        result.save()

        # create a choice for this trial,
        # this shows the door choice they've made
        choice_one = Choice()
        choice_one.door_number = 1
        choice_one.first_or_second_choice = 1
        choice_one.trial = trial
        choice_one.save()

        choice_two = Choice()
        choice_two.door_number = 1
        choice_two.first_or_second_choice = 2
        choice_two.trial = trial
        choice_two.save()


        self.assertEqual('temporary',user.username)
        response_client = self.client.get('/user/temporary/final-door-result', follow=True)
        self.assertTemplateUsed(response_client,'regret.html')


    def test_final_door_result_page_returns_correct_html(self):
        self.login_temp()
        user = User.objects.get(username='temporary')
        # An associated trial also needs to be created
        # as this is usually created by the view:
        # memory_game_initial_turn
        trial = Trial()
        trial.user = user
        trial.number_of_trial = 1
        trial.save()

        #response = self.client.get('/user/temporary/door-result', follow=True)
        request = HttpRequest()
        request.method = "GET"
        request.user = user

        response = final_door_result_page(request, user.username)
        html = response.content.decode('utf8')
        self.assertIn('The result of your final door choice', html)

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

    def test_first_result_page_can_display_a_POST_request(self):
        self.login_temp()
        response_home = self.client.post(
            '/user/temporary/door_page_one', {'door_chosen': 1}
        )
        response_first_door_result = self.client.post(
            '/user/temporary/door-result/', {'door_chosen': 1}
        )
        request = HttpRequest()
        user = User.objects.get(username='temporary')
        response_final_door_result = final_door_result_page(
            request, user.username)
        html_final_door_result = response_final_door_result.content.decode(
            'utf8')
        self.assertIn("You chose door1", html_final_door_result)
