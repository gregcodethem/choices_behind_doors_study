from django.contrib.auth.models import User

from doorgame.models import MemoryGame

from .base import BaseTest
from config.settings import TRIAL_LIMIT


class MemoryGameTest(BaseTest):

    def test_memory_game_list_created(self):
        self.login_temp()
        user = User.objects.get(username='temporary')

        response = self.client.get(
            '/memory_game_initial_turn',
            )

        memory_game_list = MemoryGame.objects.all()
        self.assertNotEqual(len(memory_game_list), 0)

    def test_number_of_memory_games_created_is_number_of_trials(self):
        self.login_temp()
        user = User.objects.get(username='temporary')

        response = self.client.get(
            '/memory_game_initial_turn',
        )
        memory_game_list = MemoryGame.objects.all()
        number_of_trials = TRIAL_LIMIT

        self.assertEqual(len(memory_game_list), number_of_trials)

class MemoryGameInitialTurnTest(BaseTest):

    def test_memory_game_initial_turn_returns_home_template(self):
        self.login_temp()

        response = self.client.get('/memory_game_initial_turn', follow=True)

        self.assertTemplateUsed(response, 'home.html')

