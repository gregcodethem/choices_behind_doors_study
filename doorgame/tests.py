from django.urls import resolve
from django.test import TestCase, Client
from django.http import HttpRequest

from doorgame.views import (
    home_page,
    home_page_user,
    home_page_user_unique,
    door_result_page,
)

from doorgame.models import Choice
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class SimpleTest(TestCase):
    def setUp(self):
        User = get_user_model()
        user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')

    def test_user_page(self):
        User = get_user_model()
        self.client.login(username='temporary', password='temporary')
        response = self.client.get('/user', follow=True)
        user = User.objects.get(username='temporary')
        #print(response.content)
        self.assertEqual(response.context['username'], 'temporary')

    def test_home_page_user_recognises_user(self):
        User = get_user_model()

        self.client.login(username='temporary', password='temporary')
        response = self.client.get('/user', follow=True)

        html = response.content.decode('utf8')
        self.assertIn('<h2>Welcome to the door game</h2>', html)
        self.assertIn('temporary', html)


class HomePageTest(TestCase):
    def setUp(self):
        User = get_user_model()
        user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')


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
        User = get_user_model()

        self.client.login(username='temporary', password='temporary')
        user = User.objects.get(username='temporary')

        response = self.client.get('/user/'+user.username+'/')
        html = response.content.decode('utf8')
        # self.assertTrue(html.startswith('<html>'))
        self.assertIn('<h2>Welcome to the door game</h2>', html)
        # self.assertTrue(html.endswith('</html>'))


    def test_can_save_a_post_request(self):
        User = get_user_model()
        self.client.login(username='temporary', password='temporary')
        user = User.objects.get(username='temporary')
        response = self.client.post(
            '/user/temporary/', {'door_chosen': 1}
        )

        self.assertEqual(Choice.objects.count(), 1)
        new_choice = Choice.objects.first()
        self.assertEqual(new_choice.door_number, 1)


    def test_saves_user_in_post_request(self):
        User = get_user_model()
        user = User.objects.get(username='temporary')
        self.client.login(username='temporary', password='temporary')
        response = self.client.post(
            '/user/temporary/', 
            {
            'door_chosen': 2,
            })
        
        self.assertEqual(Choice.objects.count(), 1)
        new_choice = Choice.objects.last()
        self.assertEqual(new_choice.door_number, 2)
        self.assertEqual(new_choice.user, user)

    def test_redirects_after_POST(self):
        User = get_user_model()
        user = User.objects.get(username='temporary')
        self.client.login(username='temporary', password='temporary')
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


class DoorResultPageTest(TestCase):
    
    def setUp(self):
        User = get_user_model()
        user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')

    def login(self):
        User = get_user_model()
        self.client.login(username='temporary', password='temporary')

    def test_door_result_url_resolves_to_door_page_view(self):
        found = resolve('/user/temporary/door-result')
        self.assertEqual(found.func, door_result_page)

    def test_door_result_page_returns_correct_html(self):
        User = get_user_model()
        self.client.login(username='temporary', password='temporary')
        user = User.objects.get(username='temporary')
        #response = self.client.get('/user/temporary/door-result', follow=True)
        request = HttpRequest()
        response = door_result_page(request, user.username)
        html = response.content.decode('utf8')
        self.assertIn('The result of your door choice', html)

    def test_can_display_a_POST_request(self):
        User = get_user_model()
        self.client.login(username='temporary', password='temporary')
        response_home = self.client.post(
            '/user/temporary/', {'door_chosen': 1}
        )
        request = HttpRequest()
        user = User.objects.get(username='temporary')
        response_door_result = door_result_page(request, user.username)
        html_door_result = response_door_result.content.decode('utf8')
        self.assertIn("You chose door1", html_door_result)

    def test_can_display_a_POST_request_for_door_two(self):
        User = get_user_model()
        self.client.login(username='temporary', password='temporary')
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
        User = get_user_model()
        self.client.login(username='temporary', password='temporary')
        user = User.objects.get(username='temporary')

        response_home = self.client.post(
            '/user/temporary/',
            data={'door_chosen': 3}
        )
        request = HttpRequest()
        User = get_user_model()
        self.client.login(username='temporary', password='temporary')
        user = User.objects.get(username='temporary')
        response_door_result = door_result_page(request, user.username)
        html_door_result = response_door_result.content.decode('utf8')
        self.assertIn("You chose door3", html_door_result)


class ChoiceModelTest(TestCase):

    def test_saving_and_retrieving_choices(self):
        user_test = User.objects.create_user(
            'george',
            '',
            'somethingpassword')
        user_test.save()
        first_choice = Choice()
        first_choice.door_number = 1
        first_choice.user = user_test
        first_choice.save()

        second_choice = Choice()
        second_choice.door_number = 2
        second_choice.user = user_test
        second_choice.save()

        saved_choices = Choice.objects.all()
        self.assertEqual(saved_choices.count(), 2)

        first_saved_choice = saved_choices[0]
        second_saved_choice = saved_choices[1]
        self.assertEqual(first_saved_choice.door_number, 1)
        self.assertEqual(second_saved_choice.door_number, 2)

    def test_saving_and_retrieving_user_name_from_choices(self):
        user_test_one = User.objects.create_user(
            'george',
            '',
            'somethingpassword')
        user_test_one.save()
        first_choice = Choice()
        first_choice.door_number = 1
        first_choice.user = user_test_one
        first_choice.save()

        user_test_two = User.objects.create_user(
            'brian',
            '',
            'not-the-messiah')
        user_test_two.save()
        second_choice = Choice()
        second_choice.door_number = 2
        second_choice.user = user_test_two
        second_choice.save()

        saved_choices = Choice.objects.all()
        self.assertEqual(saved_choices.count(), 2)

        first_saved_choice = saved_choices[0]
        first_saved_user = first_saved_choice.user
        second_saved_choice = saved_choices[1]
        second_saved_user = second_saved_choice.user
        self.assertEqual(first_saved_user, user_test_one)
        self.assertEqual(second_saved_user, user_test_two)
