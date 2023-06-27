from django.test import TestCase
from django.contrib.auth.models import User
from unittest import skip

from doorgame.models import (
    Trial,
    MemoryGame,
    MemoryGameHigh
)


class MemoryGameModelTest(TestCase):

    def test_saving_and_retrieving_memory_games(self):
        trial = Trial()
        trial.save()

        first_memory_game = MemoryGame()
        first_memory_game.trial = trial

        first_memory_game.save()

        saved_memory_games = MemoryGame.objects.all()
        self.assertEqual(saved_memory_games.count(), 1)
        first_saved_memory_game = saved_memory_games[0]
        first_saved_trial = first_saved_memory_game.trial
        self.assertEqual(first_saved_trial, trial)

    def test_saving_and_retrieving_boxes_from_memory_games(self):
        trial = Trial()
        trial.save()

        first_memory_game = MemoryGame()
        first_memory_game.trial = trial
        first_memory_game.box_1 = False
        first_memory_game.box_2 = True
        first_memory_game.box_3 = False
        first_memory_game.box_4 = False
        first_memory_game.box_5 = False
        first_memory_game.box_6 = False
        first_memory_game.box_7 = False
        first_memory_game.box_8 = False
        first_memory_game.box_9 = False
        
        first_memory_game.save()

        saved_memory_games = MemoryGame.objects.all()
        self.assertEqual(saved_memory_games.count(), 1)
        first_saved_memory_game = saved_memory_games[0]
        first_saved_box_1 = first_saved_memory_game.box_1
        first_saved_box_2 = first_saved_memory_game.box_2
        first_saved_box_3 = first_saved_memory_game.box_3
        first_saved_box_4 = first_saved_memory_game.box_4
        first_saved_box_5 = first_saved_memory_game.box_5
        first_saved_box_6 = first_saved_memory_game.box_6
        first_saved_box_7 = first_saved_memory_game.box_7
        first_saved_box_8 = first_saved_memory_game.box_8
        first_saved_box_9 = first_saved_memory_game.box_9

        self.assertEqual(first_saved_box_1, False)
        self.assertEqual(first_saved_box_2, True)
        self.assertEqual(first_saved_box_3, False)
        self.assertEqual(first_saved_box_4, False)
        self.assertEqual(first_saved_box_5, False)
        self.assertEqual(first_saved_box_6, False)
        self.assertEqual(first_saved_box_7, False)
        self.assertEqual(first_saved_box_8, False)
        self.assertEqual(first_saved_box_9, False)

    def test_saving_and_retrieving_boxes_from_memory_games_four_by_four(self):
        trial = Trial()
        trial.save()

        first_memory_game = MemoryGameHigh()
        first_memory_game.trial = trial
        first_memory_game.box_1 = False
        first_memory_game.box_2 = True
        first_memory_game.box_3 = False
        first_memory_game.box_4 = False
        first_memory_game.box_5 = False
        first_memory_game.box_6 = False
        first_memory_game.box_7 = False
        first_memory_game.box_8 = False
        first_memory_game.box_9 = False
        first_memory_game.box_10 = True
        
        first_memory_game.save()

        saved_memory_games = MemoryGameHigh.objects.all()
        self.assertEqual(saved_memory_games.count(), 1)
        first_saved_memory_game = saved_memory_games[0]
        first_saved_box_1 = first_saved_memory_game.box_1
        first_saved_box_2 = first_saved_memory_game.box_2
        first_saved_box_3 = first_saved_memory_game.box_3
        first_saved_box_4 = first_saved_memory_game.box_4
        first_saved_box_5 = first_saved_memory_game.box_5
        first_saved_box_6 = first_saved_memory_game.box_6
        first_saved_box_7 = first_saved_memory_game.box_7
        first_saved_box_8 = first_saved_memory_game.box_8
        first_saved_box_9 = first_saved_memory_game.box_9
        first_saved_box_10 = first_saved_memory_game.box_10

        self.assertEqual(first_saved_box_1, False)
        self.assertEqual(first_saved_box_2, True)
        self.assertEqual(first_saved_box_3, False)
        self.assertEqual(first_saved_box_4, False)
        self.assertEqual(first_saved_box_5, False)
        self.assertEqual(first_saved_box_6, False)
        self.assertEqual(first_saved_box_7, False)
        self.assertEqual(first_saved_box_8, False)
        self.assertEqual(first_saved_box_9, False)
        self.assertEqual(first_saved_box_10, True)



    def test_saving_and_retrieving_initial_or_final_memory_games(self):
        trial = Trial()
        trial.save()

        first_memory_game = MemoryGame()
        first_memory_game.trial = trial
        first_memory_game.initial_or_final = "initial"
        first_memory_game.save()

        second_memory_game = MemoryGame()
        second_memory_game.trial = trial
        second_memory_game.initial_or_final = "final"
        second_memory_game.save()

        saved_memory_games = MemoryGame.objects.all()
        self.assertEqual(saved_memory_games.count(), 2)
        first_saved_memory_game = saved_memory_games[0]
        saved_initial = first_saved_memory_game.initial_or_final
        second_saved_memory_game = saved_memory_games[1]
        saved_final = second_saved_memory_game.initial_or_final
        self.assertEqual(saved_initial, first_saved_memory_game.initial_or_final)
        self.assertEqual(saved_final, second_saved_memory_game.initial_or_final)


