from django.urls import resolve
from django.test import Client
from django.http import HttpRequest

from doorgame.views import door_result_page, final_door_result_page

from doorgame.models import Choice, Trial, Result
from django.contrib.auth.models import User

from .test_views_base import BaseTest

from django.contrib.auth import get_user_model

class TwoUsersUseSimultaneously(BaseTest):

    def test_two_users_use_at_same_time_make_initial_choice(self):
        self.login_temp()
        User = get_user_model()
        user_one = User.objects.get(username='temporary')
        response = self.client.post(
            '/user/temporary/', {'door_chosen': 1}
        )
        self.assertEqual(Choice.objects.count(), 1)
        self.assertEqual(Trial.objects.count(), 1)

        
        user_two = User.objects.create_user('Dolores',
                                        'Dolores@lachicana.com',
                                        'por_su_abuela_catalan')
        self.client.login(username='Dolores', password='por_su_abuela_catalan')
        response = self.client.post(
            '/user/Dolores/', {'door_chosen': 2}
        )
        self.assertEqual(Choice.objects.count(), 2)
        self.assertEqual(Trial.objects.count(), 2)
        
        saved_trial_user_one = Trial.objects.get(
            user=user_one)
        saved_trial_user_two = Trial.objects.get(
            user=user_two)

        saved_choice_user_one = Choice.objects.get(
            trial=saved_trial_user_one)
        saved_choice_user_two = Choice.objects.get(
            trial=saved_trial_user_two)
        self.assertEqual(saved_choice_user_one.door_number, 1)
        self.assertEqual(saved_choice_user_two.door_number, 2)


class FinalDoorResultPageTest(BaseTest):

    def test_final_door_result_url_resolves_to_final_door_page_view(self):
        found = resolve('/user/temporary/final-door-result')
        self.assertEqual(found.func, final_door_result_page)

    def test_final_door_result_page_returns_correct_html(self):
        self.login_temp()
        user = User.objects.get(username='temporary')
        #response = self.client.get('/user/temporary/door-result', follow=True)
        request = HttpRequest()
        response = final_door_result_page(request, user.username)
        html = response.content.decode('utf8')
        self.assertIn('The result of your final door choice', html)

    def test_first_result_page_can_display_a_POST_request(self):
        self.login_temp()
        response_home = self.client.post(
            '/user/temporary/', {'door_chosen': 1}
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


class DoorResultPageTest(BaseTest):

    def test_door_result_url_resolves_to_door_page_view(self):
        found = resolve('/user/temporary/door-result')
        self.assertEqual(found.func, door_result_page)

    def test_door_result_page_returns_correct_html(self):
        self.login_temp()
        user = User.objects.get(username='temporary')
        #response = self.client.get('/user/temporary/door-result', follow=True)
        request = HttpRequest()
        response = door_result_page(request, user.username)
        html = response.content.decode('utf8')
        self.assertIn('The result of your door choice', html)

    def test_door_result_page_returns_an_incorrect_door(self):
        self.login_temp()
        user = User.objects.get(username='temporary')
        response_home = self.client.post(
            '/user/temporary/',
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
            '/user/temporary/', {'door_chosen': 1}
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
            '/user/temporary/',
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
            '/user/temporary/',
            data={'door_chosen': 3}
        )
        request = HttpRequest()
        response_door_result = door_result_page(request, user.username)
        html_door_result = response_door_result.content.decode('utf8')
        self.assertIn("You chose door3", html_door_result)
