from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from doorgame.models import (
    Choice,
    Trial,
    Result,
)
from .base import BaseTest


class TwoUsersUseSimultaneously(BaseTest):

    def test_two_users_use_at_same_time_two_choices_made_for_each_trial(self):
        self.login_temp()
        User = get_user_model()
        user_one = User.objects.get(username='temporary')

        trial_one = Trial()
        trial_one.user = user_one
        trial_one.save()

        response = self.client.post(
            '/user/temporary/door_page_one', {'door_chosen': 1}
        )
        self.assertEqual(Choice.objects.count(), 1)

        # !!---------------!!
        # Improve this test to check each choice corresdponds to the right choice

        user_two = User.objects.create_user('Dolores',
                                            'Dolores@lachicana.com',
                                            'por_su_abuela_catalan')
        self.client.login(username='Dolores', password='por_su_abuela_catalan')

        trial_two = Trial()
        trial_two.user = user_two
        trial_two.save()

        response = self.client.post(
            '/user/Dolores/door_page_one', {'door_chosen': 2}
        )
        self.assertEqual(Choice.objects.count(), 2)

    def test_two_users_use_at_same_time_make_initial_choice(self):
        self.login_temp()
        User = get_user_model()
        user_one = User.objects.get(username='temporary')

        trial_user_one = Trial()
        trial_user_one.user = user_one
        trial_user_one.number_of_trial = 1
        trial_user_one.save()

        response = self.client.post(
            '/user/temporary/door_page_one', {'door_chosen': 1}
        )

        user_two = User.objects.create_user('Dolores',
                                            'Dolores@lachicana.com',
                                            'por_su_abuela_catalan')
        trial_user_two = Trial()
        trial_user_two.user = user_two
        trial_user_two.number_of_trial = 1
        trial_user_two.save()
        self.client.login(username='Dolores', password='por_su_abuela_catalan')
        response = self.client.post(
            '/user/Dolores/door_page_one', {'door_chosen': 2}
        )

        saved_trial_user_one = Trial.objects.get(
            user=user_one)
        saved_trial_user_two = Trial.objects.get(
            user=user_two)

        saved_choice_user_one = Choice.objects.get(
            trial=saved_trial_user_one)
        saved_choice_user_two = Choice.objects.get(
            trial=saved_trial_user_two)
        self.assertEqual(saved_choice_user_one.door_number, 1)
        self.assertEqual(saved_choice_user_two.door_number, 2)

    def test_two_users_at_same_time_make_second_choice(self):
        # set up inital saved data on db
        # set up the users
        user_test_one = User.objects.create_user(
            'Acho',
            '',
            'tu_ajedrez')
        user_test_one.save()
        user_test_two = User.objects.create_user(
            'Darren',
            '',
            'just_a_sea_between_us')
        user_test_two.save()

        # set up a trial for each user
        trial_user_one = Trial()
        trial_user_one.user = user_test_one
        trial_user_one.save()
        trial_user_two = Trial()
        trial_user_two.user = user_test_two
        trial_user_two.save()

        # assign a first choice for each trial of each user
        choice_one_user_one = Choice()
        choice_one_user_one.trial = trial_user_one
        choice_one_user_one.first_or_second_choice = 1
        choice_one_user_one.door_number = 1
        choice_one_user_one.save()

        choice_one_user_two = Choice()
        choice_one_user_two.trial = trial_user_two
        choice_one_user_two.first_or_second_choice = 1
        choice_one_user_two.door_number = 2
        choice_one_user_two.save()

        # save a result for each user
        result_user_one = Result()
        result_user_one.trial = trial_user_one
        result_user_one.door_number = 3
        result_user_one.save()

        result_user_two = Result()
        result_user_two.trial = trial_user_two
        result_user_two.door_number = 1
        result_user_two.save()

        self.client.login(username='Acho', password='tu_ajedrez')
        response_one = self.client.post(
            '/doorgame/door_result', {'door_chosen': 4}
        )
        self.client.login(username='Darren',
                          password='just_a_sea_between_us'
                          )
        response_two = self.client.post(
            '/doorgame/door_result', {'door_chosen': 5}
        )

        # check has saved 2 choices for each user
        saved_choices = Choice.objects.all()
        username_list = []
        for choice in saved_choices:
            username_list.append(choice.trial.user.username)
        self.assertEqual(username_list.count('Acho'), 2)
        self.assertEqual(username_list.count('Darren'), 2)

        # retrieve saved second choices
        '''
        saved_final_choice_user_one = Choice.objects.get(
            trial=trial_user_one,
            first_or_second_choice=2
        )
        saved_final_choice_user_two = Choice.objects.get(
            trial=trial_user_two,
            first_or_second_choice=2
        )
        '''
