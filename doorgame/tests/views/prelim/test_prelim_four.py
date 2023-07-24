from unittest.mock import patch

from django.urls import resolve

from doorgame.views import prelim_four
from doorgame.models import MemoryGame

from doorgame.tests.views.base import BaseTest


class PrelimFourTest(BaseTest):
    def test_prelim_four_url_resolves_to_prelim_four_view(self):
        self.login_temp()
        found = resolve('/prelim_four')
        self.assertEqual(found.func, prelim_four)


    def test_prelim_four_user_sees_prelim_four_page(self):
        self.login_temp()

        response = self.client.get('/prelim_four', follow=True)

        html = response.content.decode('utf8')
        self.assertIn('Now play the memory task', html)

    def test_prelim_four_returns_prelim_four_template(self):
        self.login_temp()

        response = self.client.get('/prelim_four', follow=True)
        self.assertTemplateUsed(response, 'prelim/prelim_four.html')

    def test_prelim_four_returns_continue_message(self):
        self.login_temp()

        response = self.client.get(
            '/prelim_four',
            follow=True,
        )
        html = response.content.decode('utf8')

        # test desired continue message is displayed:
        self.assertIn('Continue to next page',html)


    def test_prelim_four_contains_links_to_correct_page(self):
        self.login_temp()

        response = self.client.get(
            '/prelim_four',
            follow=True,
        )
        html = response.content.decode('utf8')

        self.assertIn('href= /prelim_five', html)