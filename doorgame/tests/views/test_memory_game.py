from django.contrib.auth.models import User

from doorgame.models import (
    MemoryGame,
    MemoryGameList,
    Trial,
    Choice,
)
from doorgame.utils import add_memory_games

from .base import BaseTest
from .test_door_result_one import DoorResultPageTest
from config.settings import TRIAL_LIMIT


class MemoryGameTest(BaseTest):

    def test_memory_game_list_created(self):
        self.login_temp()
        user = User.objects.get(username='temporary')

        response = self.client.get(
            '/memory_game/memory_game_initial_turn',
            )

        memory_game_list = MemoryGame.objects.all()
        self.assertNotEqual(len(memory_game_list), 0)

    def test_number_of_memory_games_created_is_number_of_trials(self):
        self.login_temp()
        user = User.objects.get(username='temporary')

        response = self.client.get(
            '/memory_game/memory_game_initial_turn',
        )
        memory_game_list = MemoryGame.objects.all()
        number_of_trials = TRIAL_LIMIT

        self.assertEqual(len(memory_game_list), number_of_trials)

class MemoryGameInitialTurnTest(BaseTest):

    def test_memory_game_initial_turn_returns_home_template(self):
        self.login_temp()

        response = self.client.get('/memory_game/memory_game_initial_turn', follow=True)

        self.assertTemplateUsed(response, 'memory_game/home.html')

class MemoryGameFinalPatternTest(DoorResultPageTest):


    def test_final_pattern_url_redirects_to_final_door_result(self):
        self.login_temp()
        user = User.objects.get(username='temporary')

        # An associated trial also needs to be created
        # as this is usually created by the view:
        # memory_game_initial_turn
        trial = Trial()
        trial.user = user
        trial.number_of_trial = 1
        trial.save()

        response = self.client.post(
            '/memory_game/final_pattern',
            {
                'box_1': True,
                'box_2': True,
                'box_3': True
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/doorgame/outcome_of_doorgame')

    def test_final_pattern_url_saves_memory_game_box_choices(self):
        self.login_temp()
        user = User.objects.get(username='temporary')

        # An associated trial also needs to be created
        # as this is usually created by the view:
        # memory_game_initial_turn
        trial = Trial()
        trial.user = user
        trial.number_of_trial = 1
        trial.save()

        memory_game_list = MemoryGameList()
        memory_game_list.user = user
        memory_game_list.save()
        add_memory_games(memory_game_list, "easy")

        response = self.client.post(
            '/memory_game/final_pattern',
            {
                'box_1': True,
                'box_2': True,
                'box_3': True
            }
        )

        trial = Trial.objects.filter(user=user).last()
        memory_game_existing_objects = MemoryGame.objects.filter(trial=trial)
        final_memory_game = memory_game_existing_objects.last()
        saved_box_1 = final_memory_game.box_1
        saved_box_2 = final_memory_game.box_2
        saved_box_3 = final_memory_game.box_3
        saved_box_4 = final_memory_game.box_4

        self.assertEqual(final_memory_game.initial_or_final, 'final')
        self.assertEqual(saved_box_1, True)
        self.assertEqual(saved_box_2, True)
        self.assertEqual(saved_box_3, True)
        self.assertEqual(saved_box_4, False)



