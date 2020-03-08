from django.urls import resolve
from django.test import TestCase, Client
from django.http import HttpRequest

from doorgame.views import (
    home_page,
    home_page_user,
    home_page_user_unique,
    door_result_page,
)

from doorgame.models import Choice, Trial, Result
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

class BaseTest(TestCase):
    def setUp(self):
        User = get_user_model()
        user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')

    def login_temp(self):
        User = get_user_model()
        self.client.login(username='temporary', password='temporary')


class SimpleTest(BaseTest):
    
    def test_user_page(self):
        self.login_temp()
        response = self.client.get('/user', follow=True)
        user = User.objects.get(username='temporary')
        #print(response.content)
        self.assertEqual(response.context['username'], 'temporary')

    def test_home_page_user_recognises_user(self):
        self.login_temp()
        response = self.client.get('/user', follow=True)

        html = response.content.decode('utf8')
        self.assertIn('<h2>Welcome to the door game</h2>', html)
        self.assertIn('temporary', html)


class ResultTest(BaseTest):

    def test_result_recorded_when_choice_made(self):
        self.login_temp()
        user = User.objects.get(username='temporary')
        response = self.client.post(
            '/user/temporary/', 
            {
            'door_chosen': 2,
            })
        self.assertEqual(Result.objects.count(), 1)
        result = Result.objects.first()
        self.assertIn(result.door_number, [1,2,3])

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

    def test_home_page_returns_correct_html(self):
        self.login_temp()
        user = User.objects.get(username='temporary')

        response = self.client.get('/user/'+user.username+'/')
        html = response.content.decode('utf8')
        # self.assertTrue(html.startswith('<html>'))
        self.assertIn('<h2>Welcome to the door game</h2>', html)
        # self.assertTrue(html.endswith('</html>'))


    def test_can_save_a_post_request(self):
        self.login_temp()
        user = User.objects.get(username='temporary')
        response = self.client.post(
            '/user/temporary/', {'door_chosen': 1}
        )

        self.assertEqual(Choice.objects.count(), 1)
        new_choice = Choice.objects.first()
        self.assertEqual(new_choice.door_number, 1)


    def test_saves_user_in_post_request(self):
        self.login_temp()
        user = User.objects.get(username='temporary')
        response = self.client.post(
            '/user/temporary/', 
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
            '/user/temporary/', {'door_chosen': 1}
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/user/temporary/door-result')


    def test_only_saves_door_choices_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Choice.objects.count(), 0)


class LoginScreenTest(TestCase):

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
