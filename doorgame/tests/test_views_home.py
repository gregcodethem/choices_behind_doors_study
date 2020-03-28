from unittest import skip

from django.urls import resolve
from django.test import Client
from django.http import HttpRequest

from doorgame.views import (
    home_page,
    home_page_user,
    home_page_user_unique,
)

from doorgame.models import Choice, Trial, Result, MemoryGame
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from .test_views_base import BaseTest


class SimpleTest(BaseTest):

    def test_user_page(self):
        self.login_temp()
        response = self.client.get('/user', follow=True)
        user = User.objects.get(username='temporary')
        # print(response.content)
        self.assertEqual(response.context['username'], 'temporary')

    def test_home_page_user_recognises_user(self):
        self.login_temp()
        response = self.client.get('/user', follow=True)

        html = response.content.decode('utf8')
        self.assertIn('<h2>Can you remember these dots?</h2>', html)
        self.assertIn('temporary', html)

class TrialNumberTest(BaseTest):

    def test_home_page_gives_trial_number(self):
        self.login_temp()
        response = self.client.get('/user', follow=True)

        html = response.content.decode('utf8')
        self.assertIn('Trial number 1', html)

    def test_home_page_gives_trial_number_two_for_second_trial(self):
        user_test = User.objects.create_user(
            'george',
            '',
            'somethingpassword')
        user_test.save()
        first_trial = Trial()
        first_trial.user = user_test
        first_trial.number_of_trial = 1
        first_trial.save()

        #User = get_user_model()
        self.client.login(username='george', password='somethingpassword')
        response = self.client.get('/user', follow=True)

        html = response.content.decode('utf8')
        self.assertIn('Trial number 2', html)

    def test_trial_number_created_when_memory_game_accessed(self):
        self.login_temp()
        user = User.objects.get(username='temporary')
        response = self.client.get(
            '/user/temporary/',
            )
        trials_list = Trial.objects.all()
        trial_created = Trial.objects.last()
        number_of_trial = trial_created.number_of_trial

        self.assertEqual(number_of_trial, 1)


class MemoryGameTest(BaseTest):

    def test_memory_game_saved_when_seeing_it(self):
        self.login_temp()
        user = User.objects.get(username='temporary')
        response = self.client.get(
            '/user/temporary/',
            )
        memory_game_list = MemoryGame.objects.all()
        self.assertEqual(len(memory_game_list), 1)


class ResultTest(BaseTest):

    def test_result_recorded_when_choice_made(self):
        self.login_temp()
        user = User.objects.get(username='temporary')
        response = self.client.post(
            '/user/temporary/door_page_one',
            {
                'door_chosen': 2,
            })
        self.assertEqual(Result.objects.count(), 1)
        result = Result.objects.first()
        self.assertIn(result.door_number, [1, 2, 3])


class HomePageTest(BaseTest):

    def test_can_login(self):
        user_test = User.objects.create_user(
            'george')
        user_test.set_password('12345ham1234')
        user_test.save()

        logged_in = self.client.login(
            username='george',
            password='12345ham1234'
        )
        self.assertTrue(logged_in)

    # change to wherever the doorgame is
    def test_door_game_page_returns_correct_html(self):
        self.login_temp()
        user = User.objects.get(username='temporary')

        response = self.client.get('/user/' + user.username + '/door_page_one')
        html = response.content.decode('utf8')
        # self.assertTrue(html.startswith('<html>'))
        self.assertIn('<h2>Welcome to the door game</h2>', html)
        # self.assertTrue(html.endswith('</html>'))

    def test_home_page_returns_correct_html(self):
        self.login_temp()
        user = User.objects.get(username='temporary')

        response = self.client.get('/user/' + user.username + '/')
        html = response.content.decode('utf8')
        # self.assertTrue(html.startswith('<html>'))
        self.assertIn('<h2>Can you remember these dots?</h2>', html)
        # self.assertTrue(html.endswith('</html>'))

    def test_home_page_redirects_to_door_page_one(self):
        self.login_temp()
        user = User.objects.get(username='temporary')

        response = self.client.post(
            '/user/' + user.username + '/',
            {'pattern_at_start': 1}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/user/temporary/door-page-one')



class DoorToChooseTest(BaseTest):

    def test_can_save_a_post_request(self):
        self.login_temp()
        user = User.objects.get(username='temporary')
        response = self.client.post(
            '/user/temporary/door_page_one', {'door_chosen': 1}
        )

        self.assertEqual(Choice.objects.count(), 1)
        new_choice = Choice.objects.first()
        self.assertEqual(new_choice.door_number, 1)

    def test_saves_user_in_post_request(self):
        self.login_temp()
        user = User.objects.get(username='temporary')
        trial = Trial()
        trial.user = user
        trial.number_of_trial = 1
        trial.save()

        response = self.client.post(
            '/user/temporary/door_page_one',
            {
                'door_chosen': 2,
            })

        self.assertEqual(Choice.objects.count(), 1)
        new_choice = Choice.objects.last()
        self.assertEqual(new_choice.door_number, 2)
        trial = new_choice.trial
        self.assertEqual(trial.user, user)

    def test_redirects_after_POST(self):
        self.login_temp()
        user = User.objects.get(username='temporary')
        response = self.client.post(
            '/user/temporary/door_page_one', {'door_chosen': 1}
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/user/temporary/door-result')

    def test_only_saves_door_choices_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Choice.objects.count(), 0)


class LoginScreenTest(BaseTest):

    def test_login_screen_redirects_to_account_url(self):
        user = User.objects.create_user(
            'george',
            '',
            'somethingpassword')
        user.save()
        response = self.client.post(
            '/accounts/login',
            {"id_username": 'george',
             "id_password": "somethingpassword"
             }
        )

        #self.assertEqual(response.status_code, 302)
        #self.assertEqual(response['location'], '/user/george')
