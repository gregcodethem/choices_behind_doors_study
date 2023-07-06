from unittest.mock import patch

from django.urls import resolve

from doorgame.views import prelim_five
from doorgame.models import MemoryGame

from .base import BaseTest


class PrelimFiveTest(BaseTest):
    def test_prelim_five_url_resolves_to_prelim_five_view(self):
        self.login_temp()
        found = resolve('/prelim_five')
        self.assertEqual(found.func, prelim_five)


    def test_prelim_five_user_sees_prelim_five_page(self):
        self.login_temp()

        response = self.client.get('/prelim_five', follow=True)

        html = response.content.decode('utf8')
        self.assertIn('Now play the memory task', html)

    def test_prelim_five_returns_prelim_five_template(self):
        self.login_temp()

        response = self.client.get('/prelim_five', follow=True)
        self.assertTemplateUsed(response, 'prelim_five.html')

    def test_prelim_five_returns_continue_message(self):
        self.login_temp()

        response = self.client.get(
            '/prelim_five',
            follow=True,
        )
        html = response.content.decode('utf8')

        # test desired continue message is displayed:
        self.assertIn("Let's play the game",html)


    def test_prelim_five_contains_links_to_correct_page(self):
        self.login_temp()

        response = self.client.get(
            '/prelim_five',
            follow=True,
        )
        html = response.content.decode('utf8')

        self.assertIn('href= /memory_game_initial_turn', html)