from django.urls import resolve, reverse
from django.http import HttpRequest
from django.contrib.auth.models import User

from doorgame.views import door_result_page
from .base import BaseTest

class DoorResultPageTest(BaseTest):

    def test_door_result_url_resolves_to_door_page_view(self):
        found = resolve('/user/temporary/door-result')
        self.assertEqual(found.func, door_result_page)

    def test_door_result_page_returns_correct_html(self):
        #!!!!!!
        #!!!!! This test is what I need to rewrite,
        # I need to look at the actual view
        # and think what it is I want to be testing
        # do i need to do more in the setup?
        # needs a good think


        self.login_temp()
        user = User.objects.get(username='temporary')
        # create a trial for this user


        # create a choice for this trial

        # response = self.client.get('/user/temporary/door-result', follow=True)
        request = HttpRequest()
        request.method = 'POST'
        request.user = user
        response = door_result_page(request, user.username)
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
