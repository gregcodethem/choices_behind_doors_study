from django.contrib.auth.models import User
from django.urls import reverse

from doorgame.models import (
    Choice,
    Trial,
    Result,
)

from .base import BaseTest

class DoorGameTest(BaseTest):

    def test_door_page_one_returns_door_page_one_template(self):
        self.login_temp()

        response = self.client.get('/door_page_one', follow=True)

        self.assertTemplateUsed(response, 'doorgame/door_page_one.html')


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
            '/choose_door', {'door_chosen': 1}
        )

        self.assertEqual(Choice.objects.count(), 1)
        new_choice = Choice.objects.first()
        self.assertEqual(new_choice.door_number, 1)

    def test_choose_door_redirects_to_door_result_page(self):
        self.login_temp()
        user = User.objects.get(username='temporary')

        response = self.client.post(
            '/choose_door', {'door_chosen': 1}
        )

        self.assertRedirects(response, reverse('door_result_page',kwargs={'username': 'temporary'}))

    def test_saves_user_in_post_request(self):
        self.login_temp()
        user = User.objects.get(username='temporary')
        trial = Trial()
        trial.user = user
        trial.number_of_trial = 1
        trial.save()

        response = self.client.post(
            '/choose_door',
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
            '/choose_door', {'door_chosen': 1}
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
