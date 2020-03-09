from django.test import TestCase
from django.contrib.auth.models import User
from unittest import skip

from doorgame.models import (
    Choice,
    Trial,
    Result,
    MemoryGame
)


class ResultModelTest(TestCase):

    def test_saving_and_retrieving_results(self):
        user_test = User.objects.create_user(
            'george',
            '',
            'somethingpassword')
        user_test.save()
        first_result = Result()
        first_result.door_number = 3
        first_result.save()

        second_result = Result()
        second_result.door_number = 2
        second_result.save()

        saved_results = Result.objects.all()
        self.assertEqual(saved_results.count(), 2)

        first_saved_result = saved_results[0]
        second_saved_result = saved_results[1]
        self.assertEqual(first_saved_result.door_number, 3)
        self.assertEqual(second_saved_result.door_number, 2)

    # not sure if I need to save two types of results,
    # keep this here for now for base of chocie tests
    @skip
    def test_saving_and_retrieving_final_results_keeps_same_door_number(self):
        user_test = User.objects.create_user(
            'george',
            '',
            'somethingpassword')
        user_test.save()
        trial = Trial()
        trial.user = user_test
        trial.save()
        first_result = Result()
        first_result.door_number = 3
        first_result.first_or_second_choice = 1
        first_result.trial = trial
        first_result.save()

        # keeps same number
        final_result = Result()
        final_result.door_number = 3
        final_result.first_or_second_choice = 2
        final_result.trial = trial
        final_result.save()

        first_saved_result = Result.objects.get(
            trial=trial,
            first_or_second_choice=1
        )
        final_saved_result = Result.objects.get(
            trial=trial,
            first_or_second_choice=2
        )

        self.assertEqual(first_saved_result.door_number, 3)
        self.assertEqual(first_saved_result.first_or_second_choice, 1)
        self.assertEqual(final_saved_result.door_number, 3)
        self.assertEqual(final_saved_result.first_or_second_choice, 2)

    def test_result_saves_trial(self):
        user_test = User.objects.create_user(
            'george',
            '',
            'somethingpassword')
        user_test.save()
        first_trial = Trial()
        first_trial.user = user_test
        first_trial.save()
        first_result = Result()
        first_result.trial = first_trial
        first_result.save()

        saved_results = Result.objects.all()
        self.assertEqual(saved_results.count(), 1)
        first_saved_result = saved_results[0]
        first_saved_trial = first_saved_result.trial
        self.assertEqual(first_saved_trial, first_trial)


class TrialModelTest(TestCase):

    def test_saving_and_retrieving_trials(self):
        user_test = User.objects.create_user(
            'george',
            '',
            'somethingpassword')
        user_test.save()
        first_trial = Trial()
        first_trial.user = user_test
        first_trial.save()

        saved_trials = Trial.objects.all()
        self.assertEqual(saved_trials.count(), 1)
        first_saved_trial = saved_trials[0]
        first_saved_user = first_saved_trial.user
        self.assertEqual(first_saved_user, user_test)


class MemoryGameModelTest(TestCase):

    def test_saving_and_retrieving_memory_games(self):
        user_test = User.objects.create_user(
            'george',
            '',
            'somethingpassword')
        user_test.save()
        first_memory_game = MemoryGame()
        first_memory_game.user = user_test
        first_memory_game.save()

        saved_memory_games = MemoryGame.objects.all()
        self.assertEqual(saved_memory_games.count(), 1)
        first_saved_memory_game = saved_memory_games[0]
        first_saved_user = first_saved_memory_game.user
        self.assertEqual(first_saved_user, user_test)


class ChoiceModelTest(TestCase):

    def test_saving_and_retrieving_choices(self):
        user_test = User.objects.create_user(
            'george',
            '',
            'somethingpassword')
        user_test.save()
        first_choice = Choice()
        first_choice.door_number = 1
        first_choice.save()

        second_choice = Choice()
        second_choice.door_number = 2
        second_choice.save()

        saved_choices = Choice.objects.all()
        self.assertEqual(saved_choices.count(), 2)

        first_saved_choice = saved_choices[0]
        second_saved_choice = saved_choices[1]
        self.assertEqual(first_saved_choice.door_number, 1)
        self.assertEqual(second_saved_choice.door_number, 2)


    def test_saving_and_retrieving_final_choices_keeps_same_door_number(self):
        user_test = User.objects.create_user(
            'george',
            '',
            'somethingpassword')
        user_test.save()
        trial = Trial()
        trial.user = user_test
        trial.save()
        first_choice = Choice()
        first_choice.door_number = 3
        first_choice.first_or_second_choice = 1
        first_choice.trial = trial
        first_choice.save()

        # keeps same number
        final_choice = Choice()
        final_choice.door_number = 3
        final_choice.first_or_second_choice = 2
        final_choice.trial = trial
        final_choice.save()

        first_saved_choice = Choice.objects.get(
            trial=trial,
            first_or_second_choice=1
        )
        final_saved_choice = Choice.objects.get(
            trial=trial,
            first_or_second_choice=2
        )

        self.assertEqual(first_saved_choice.door_number, 3)
        self.assertEqual(first_saved_choice.first_or_second_choice, 1)
        self.assertEqual(final_saved_choice.door_number, 3)
        self.assertEqual(final_saved_choice.first_or_second_choice, 2)


    def test_saving_and_retrieving_user_name_from_choices(self):
        user_test_one = User.objects.create_user(
            'george',
            '',
            'somethingpassword')
        user_test_one.save()
        first_trial = Trial()
        first_trial.user = user_test_one
        first_trial.save()
        first_choice = Choice()
        first_choice.door_number = 1
        first_choice.trial = first_trial
        first_choice.save()

        user_test_two = User.objects.create_user(
            'brian',
            '',
            'not-the-messiah')
        user_test_two.save()
        second_trial = Trial()
        second_trial.user = user_test_two
        second_trial.save()
        second_choice = Choice()
        second_choice.door_number = 2
        second_choice.trial = second_trial
        second_choice.save()

        saved_choices = Choice.objects.all()
        self.assertEqual(saved_choices.count(), 2)

        first_saved_choice = saved_choices[0]
        first_saved_trial = first_saved_choice.trial
        first_saved_user = first_saved_trial.user
        second_saved_choice = saved_choices[1]
        second_saved_trial = second_saved_choice.trial
        second_saved_user = second_saved_trial.user

        self.assertEqual(first_saved_user, user_test_one)
        self.assertEqual(second_saved_user, user_test_two)

    def test_choice_saves_trial(self):
        user_test = User.objects.create_user(
            'george',
            '',
            'somethingpassword')
        user_test.save()
        first_trial = Trial()
        first_trial.user = user_test
        first_trial.save()

        first_choice = Choice()
        first_choice.trial = first_trial
        first_choice.save()

        saved_choices = Choice.objects.all()
        self.assertEqual(saved_choices.count(), 1)
        first_saved_choice = saved_choices[0]
        first_saved_trial = first_saved_choice.trial
        self.assertEqual(first_saved_trial, first_trial)
