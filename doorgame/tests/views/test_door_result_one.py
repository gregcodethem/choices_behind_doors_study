from django.urls import resolve, reverse
from django.http import HttpRequest
from django.contrib.auth.models import User

from doorgame.views import door_result_page
from doorgame.models import (
    Trial,
    Choice,
    Result
)
from .base import BaseTest

class DoorResultPageTest(BaseTest):

    def door_result_page_login_and_model_setup(
            self,
            choose_door_url_to_be_called=True
    ):
        self.login_temp()
        user = User.objects.get(username='temporary')

        # An associated trial also needs to be created
        # as this is usually created by the view:
        # memory_game_initial_turn
        trial = Trial()
        trial.user = user
        trial.number_of_trial = 1
        trial.save()

        if choose_door_url_to_be_called == False:
            # The result of the door game, needs to be fed into
            # this view, so an instance of this needs to be created here
            result = Result()
            result.trial = trial
            result.door_number = 1
            result.save()

            # create a choice for this trial,
            # this shows the door choice they've made
            choice = Choice()
            choice.door_number = 1
            choice.first_or_second_choice = 1
            choice.trial = trial
            choice.save()

    def test_door_result_url_resolves_to_door_page_view(self):
        found = resolve('/user/temporary/door-result')
        self.assertEqual(found.func, door_result_page)

    def test_door_result_view_returns_correct_html(self):
        # For this to work various different
        # model instances are created by this setup method
        # the model instances will be referenced by the view
        self.door_result_page_login_and_model_setup(
            choose_door_url_to_be_called=False
        )

        user = User.objects.get(username='temporary')

        request = HttpRequest()
        request.method = 'GET'
        request.user = user

        response = door_result_page(request, user.username)
        html = response.content.decode('utf8')

        self.assertIn('The result of your door choice', html)

    def test_door_result_page_returns_correct_html(self):
        # Sister test to test_door_result_view_returns_correct_html
        # but testing from the url
        # For this to work various different
        # model instances are created by this setup method
        # the model instances will be referenced by the view
        self.door_result_page_login_and_model_setup(
            choose_door_url_to_be_called=False
        )

        response = self.client.get('/user/temporary/door-result', follow=True)

        html = response.content.decode('utf8')
        self.assertIn('The result of your door choice', html)

    def test_door_result_page_returns_an_incorrect_door(self):

        self.door_result_page_login_and_model_setup(
            choose_door_url_to_be_called=True
        )
        user = User.objects.get(username='temporary')

        # this method will assign a chosen door,
        # it will also create a result instance as part of
        # it's logic, so no result model instance needs to be called here
        response_door_page_one = self.client.post(
            '/choose_door',
            data={'door_chosen': 3}
        )

        request = HttpRequest()
        request.method = 'GET'
        request.user = user

        response_door_result_page = door_result_page(request, user.username)
        html_door_result = response_door_result_page.content.decode('utf8')

        # Check that the door_goat image is displayed for
        # door 1 or door 2
        # the image contains an alt attribute of the form:
        # alt="open_door_goat2"
        self.assertRegex(html_door_result, '.*door_goat(1|2).*')
        # check that there is no goat image for door 3:
        self.assertNotIn('alt="open_door_goat3"', html_door_result)

    def test_can_display_a_POST_request(self):

        self.door_result_page_login_and_model_setup(
            choose_door_url_to_be_called=True
        )

        user = User.objects.get(username='temporary')

        # this method will assign a chosen door,
        # it will also create a result instance as part of
        # it's logic, so no result model instance needs to be called here
        response_home = self.client.post(
            '/choose_door', {'door_chosen': 1}
        )

        request = HttpRequest()
        request.method = 'GET'
        request.user = user

        response_door_result = door_result_page(request, user.username)
        html_door_result = response_door_result.content.decode('utf8')

        self.assertIn('alt="door 1 chosen"', html_door_result)

    def test_can_display_a_POST_request_for_door_two(self):

        self.door_result_page_login_and_model_setup(
            choose_door_url_to_be_called=True
        )

        user = User.objects.get(username='temporary')

        # this method will assign a chosen door,
        # it will also create a result instance as part of
        # it's logic, so no result model instance needs to be called here
        response_home = self.client.post(
            '/choose_door', {'door_chosen': 2}
        )

        request = HttpRequest()
        request.method = 'GET'
        request.user = user

        response_door_result = door_result_page(request, user.username)
        html_door_result = response_door_result.content.decode('utf8')

        self.assertIn('alt="door 2 chosen"', html_door_result)

    def test_can_display_a_POST_request_for_door_three(self):
        self.door_result_page_login_and_model_setup(
            choose_door_url_to_be_called=True
        )

        user = User.objects.get(username='temporary')

        # this method will assign a chosen door,
        # it will also create a result instance as part of
        # it's logic, so no result model instance needs to be called here
        response_home = self.client.post(
            '/choose_door', {'door_chosen': 3}
        )

        request = HttpRequest()
        request.method = 'GET'
        request.user = user

        response_door_result = door_result_page(request, user.username)
        html_door_result = response_door_result.content.decode('utf8')

        self.assertIn('alt="door 3 chosen"', html_door_result)
