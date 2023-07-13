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

    def test_door_result_url_resolves_to_door_page_view(self):
        found = resolve('/user/temporary/door-result')
        self.assertEqual(found.func, door_result_page)

    def test_door_result_view_returns_correct_html(self):
        # For this to work I need to create various different
        # model instances which will be referenced by the view

        self.login_temp()
        # For this to work, I need to create a user,
        user = User.objects.get(username='temporary')

        # set their profile hard_or_easy setting,
        # or their low_medium_or_high_dots_setting if it's
        # a 4 by 4 memory game
        profile = user.profile
        profile.hard_or_easy_dots = 'easy'
        profile.save()

        # An associated trial also needs to be created
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
        choice = Choice()
        choice.door_number = 1
        choice.first_or_second_choice = 1
        choice.trial = trial
        choice.save()

        request = HttpRequest()
        request.method = 'GET'
        request.user = user

        response = door_result_page(request, user.username)
        html = response.content.decode('utf8')

        self.assertIn('The result of your door choice', html)

    def test_door_result_page_returns_correct_html(self):
        # Sister test to test_door_result_view_returns_correct_html
        # but testing from the url
        # For this to work I need to create various different
        # model instances which will be referenced by the view

        self.login_temp()
        # For this to work, I need to create a user,
        user = User.objects.get(username='temporary')

        # set their profile hard_or_easy setting,
        # or their low_medium_or_high_dots_setting if it's
        # a 4 by 4 memory game
        profile = user.profile
        profile.hard_or_easy_dots = 'easy'
        profile.save()

        # An associated trial also needs to be created
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
        choice = Choice()
        choice.door_number = 1
        choice.first_or_second_choice = 1
        choice.trial = trial
        choice.save()

        response = self.client.get('/user/temporary/door-result', follow=True)

        html = response.content.decode('utf8')
        self.assertIn('The result of your door choice', html)

    def test_door_result_page_returns_an_incorrect_door(self):
        self.login_temp()
        user = User.objects.get(username='temporary')
        response_home = self.client.post(
            '/user/temporary/door_page_one',
            data={'door_chosen': 3}
        )
        request = HttpRequest()
        user = User.objects.get(username='temporary')
        response_door_result = door_result_page(request, user.username)
        html_door_result = response_door_result.content.decode('utf8')
        self.assertRegex(html_door_result, '.*door(1|2).*')

    def test_can_display_a_POST_request(self):
        self.login_temp()
        response_home = self.client.post(
            '/user/temporary/door_page_one', {'door_chosen': 1}
        )
        request = HttpRequest()
        user = User.objects.get(username='temporary')
        response_door_result = door_result_page(request, user.username)
        html_door_result = response_door_result.content.decode('utf8')
        self.assertIn("You chose door1", html_door_result)

    def test_can_display_a_POST_request_for_door_two(self):
        self.login_temp()
        user = User.objects.get(username='temporary')
        # add for door 2
        response_home = self.client.post(
            '/user/temporary/door_page_one',
            data={'door_chosen': 2}

        )
        request = HttpRequest()
        response_door_result = door_result_page(request, user.username)
        html_door_result = response_door_result.content.decode('utf8')
        self.assertIn("You chose door2", html_door_result)

    def test_can_display_a_POST_request_for_door_three(self):
        self.login_temp()
        user = User.objects.get(username='temporary')

        response_home = self.client.post(
            '/user/temporary/door_page_one',
            data={'door_chosen': 3}
        )
        request = HttpRequest()
        response_door_result = door_result_page(request, user.username)
        html_door_result = response_door_result.content.decode('utf8')
        self.assertIn("You chose door3", html_door_result)
