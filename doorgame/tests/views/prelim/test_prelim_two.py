from unittest.mock import patch

from django.urls import resolve

from doorgame.views import prelim_two
from doorgame.models import MemoryGame

from doorgame.tests.views.base import BaseTest


class PrelimTwoTest(BaseTest):
    def test_prelim_two_url_resolves_to_prelim_two_view(self):
        self.login_temp()
        found = resolve('/prelim_memory_game/prelim_two')
        self.assertEqual(found.func, prelim_two)

    def test_prelim_two_user_sees_prelim_two_page(self):
        self.login_temp()

        response = self.client.get('/prelim_memory_game/prelim_two', follow=True)

        html = response.content.decode('utf8')
        self.assertIn('<div class="row no-gutters">', html)

    def test_prelim_two_returns_prelim_two_template(self):
        self.login_temp()

        response = self.client.get('/prelim_memory_game/prelim_two', follow=True)
        self.assertTemplateUsed(response, 'prelim_memory_game/prelim_two.html')


    def test_prelim_two_returns_dot_in_grid(self):
        self.login_temp()

        response = self.client.get('/prelim_memory_game/prelim_two', follow=True)
        html = response.content.decode('utf8')

        self.assertIn('<img src="/static/doorgame/box_with_dot.png"', html)

    @patch('doorgame.views.MemoryGamePrelimClassNineByNine')
    def test_prelim_two_uses_memory_game_prelim_class(self, MockMemoryGamePrelimClassNineByNine):
        self.login_temp()

        # Mock the constructor of MemoryGamePrelimClassNineByNine
        mock_game = MockMemoryGamePrelimClassNineByNine.return_value

        response = self.client.get('/prelim_memory_game/prelim_two', follow=True)

        # Assert that MemoryGamePrelimClass was instantiated
        self.assertTrue(MockMemoryGamePrelimClassNineByNine.called)



class PrelimTwoFourByFourTest(BaseTest):

    def test_prelim_two_four_by_four_user_sees_prelim_two_four_by_four_page(self):
        self.login_temp()

        self.set_to_four_by_four()

        response = self.client.get('/prelim_memory_game/prelim_two', follow=True)

        html = response.content.decode('utf8')
        self.assertIn('<div class="row no-gutters">', html)

    def test_prelim_two_four_by_four_returns_prelim_two_four_by_four_template(self):
        self.login_temp()

        self.set_to_four_by_four()

        response = self.client.get('/prelim_memory_game/prelim_two', follow=True)
        self.assertTemplateUsed(response, 'prelim_memory_game/prelim_two_four_by_four.html')

    def test_prelim_two_four_by_four_returns_dot_in_grid(self):
        self.login_temp()

        self.set_to_four_by_four()

        response = self.client.get('/prelim_memory_game/prelim_two', follow=True)
        html = response.content.decode('utf8')

        self.assertIn('<img src="/static/doorgame/box_with_dot.png"', html)

    @patch('doorgame.views.MemoryGamePrelimClass')
    def test_prelim_two_four_by_four_uses_memory_game_prelim_class(self, MockMemoryGamePrelimClass):
        self.login_temp()

        # Mock the constructor of MemoryGamePrelimClassNineByNine
        mock_game = MockMemoryGamePrelimClass.return_value

        self.set_to_four_by_four()

        response = self.client.get('/prelim_memory_game/prelim_two', follow=True)

        # Assert that MemoryGamePrelimClass was instantiated
        self.assertTrue(MockMemoryGamePrelimClass.called)

