from django.urls import resolve
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from doorgame.views import final_door_result_page
from doorgame.models import (
    Choice,
    Trial,
    Result,
    MemoryGame,
)
from .base import BaseTest
from .test_door_result_one import DoorResultPageTest


class FinalPattern(BaseTest):

    def test_can_choose_final_patten(self):
        self.login_temp()
        User = get_user_model()
        user_one = User.objects.get(username='temporary')
        trial = Trial()
        trial.user = user_one
        trial.save()
        response = self.client.post(
            '/final_pattern',
            {
                'box_1': False,
                'box_2': True,
                'trial': trial,
            }
        )
        self.assertEqual(MemoryGame.objects.count(), 1)
        saved_memory_game = MemoryGame.objects.get()
        self.assertEqual(False, saved_memory_game.box_1)
        self.assertEqual(True, saved_memory_game.box_2)




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

        #!!---------------!!
        #Improve this test to check each choice corresdponds to the right choice

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
            '/user/Acho/door-result', {'door_chosen': 4}
        )
        self.client.login(username='Darren',
                          password='just_a_sea_between_us'
                          )
        response_two = self.client.post(
            '/user/Darren/door-result', {'door_chosen': 5}
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


class FinalDoorResultPageTest(BaseTest):

    def test_final_door_result_url_resolves_to_final_door_page_view(self):
        found = resolve('/user/temporary/final-door-result')
        self.assertEqual(found.func, final_door_result_page)

    def test_outcome_of_doorgame_returns_correct_html(self):
        self.login_temp()
        user = User.objects.get(username='temporary')
        # An associated trial also needs to be created
        # as this is usually created by the view:
        # memory_game_initial_turn
        trial = Trial()
        trial.user = user
        trial.number_of_trial = 1
        trial.save()

        # The result of the door game, needs to be fed into
        # this view, so an instance of this needs to be created here
        result = Result()
        result.trial = trial
        result.door_number = 1
        result.save()

        # create a choice for this trial,
        # this shows the door choice they've made
        choice_one = Choice()
        choice_one.door_number = 1
        choice_one.first_or_second_choice = 1
        choice_one.trial = trial
        choice_one.save()

        choice_two = Choice()
        choice_two.door_number = 1
        choice_two.first_or_second_choice = 2
        choice_two.trial = trial
        choice_two.save()

        response = self.client.get('/outcome_of_doorgame', follow=True)

        html = response.content.decode('utf8')
        self.assertIn('The result of your final door choice', html)

    def test_outcome_of_doorgame_returns_correct_template(self):
        self.login_temp()
        user = User.objects.get(username='temporary')
        # An associated trial also needs to be created
        # as this is usually created by the view:
        # memory_game_initial_turn
        trial = Trial()
        trial.user = user
        trial.number_of_trial = 1
        trial.save()

        # The result of the door game, needs to be fed into
        # this view, so an instance of this needs to be created here
        result = Result()
        result.trial = trial
        result.door_number = 1
        result.save()

        # create a choice for this trial,
        # this shows the door choice they've made
        choice_one = Choice()
        choice_one.door_number = 1
        choice_one.first_or_second_choice = 1
        choice_one.trial = trial
        choice_one.save()

        choice_two = Choice()
        choice_two.door_number = 1
        choice_two.first_or_second_choice = 2
        choice_two.trial = trial
        choice_two.save()

        response = self.client.get('/outcome_of_doorgame', follow=True)

        self.assertTemplateUsed(response,'final_door_result.html')

    def test_final_door_result_page_returns_correct_html(self):
        self.login_temp()
        user = User.objects.get(username='temporary')
        # An associated trial also needs to be created
        # as this is usually created by the view:
        # memory_game_initial_turn
        trial = Trial()
        trial.user = user
        trial.number_of_trial = 1
        trial.save()

        #response = self.client.get('/user/temporary/door-result', follow=True)
        request = HttpRequest()
        request.method = "GET"
        request.user = user

        response = final_door_result_page(request, user.username)
        html = response.content.decode('utf8')
        self.assertIn('The result of your final door choice', html)

class ChooseFinalDoorTest(DoorResultPageTest):
    def test_choose_final_door_method_keeping_door_redirects(self):
        self.door_result_page_login_and_model_setup()

        response = self.client.post(
            '/choose_final_door',
            {'door_chosen':1}
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/user/temporary/final-door-result')

    def test_choose_final_door_method_keeping_door_saves_choice(self):
        self.door_result_page_login_and_model_setup(
            choose_door_url_to_be_called=False
        )

        # extract model data here
        user = User.objects.get(username='temporary')
        trial = Trial.objects.filter(user=user).last()
        choice_existing_objects = Choice.objects.filter(trial=trial)
        final_door_choice = choice_existing_objects.last()
        choice_first_or_second = final_door_choice.first_or_second_choice
        choice_door_chosen = final_door_choice.door_number

        response = self.client.post(
            '/choose_final_door',
            {'final_door_chosen': 1}
        )

        # extract model data here
        user = User.objects.get(username='temporary')
        trial = Trial.objects.filter(user=user).last()
        choice_existing_objects = Choice.objects.filter(trial=trial)
        final_door_choice = choice_existing_objects.last()
        choice_first_or_second = final_door_choice.first_or_second_choice
        choice_door_chosen = final_door_choice.door_number

        self.assertEqual(len(choice_existing_objects),2)
        self.assertEqual(choice_first_or_second, 2)
        self.assertEqual(choice_door_chosen, 1)

    def test_choose_final_door_method_changing_door_redirects(self):
        # set up, this choses the first door as one by default
        self.door_result_page_login_and_model_setup(
            choose_door_url_to_be_called=False
        )
        # extract model data here
        user = User.objects.get(username='temporary')
        trial = Trial.objects.filter(user=user).last()
        result_existing_objects = Result.objects.filter(trial=trial)
        final_result = result_existing_objects.last()
        final_result_door_number = final_result.door_number

        # as we're just recording if they stick or switch
        # it dosen't matter which door they change to, only that they change
        response_change_to_two = self.client.post(
            '/choose_final_door',
            {'door_chosen':2}
        )

        self.assertEqual(response_change_to_two.status_code, 302)
        self.assertEqual(response_change_to_two['location'], '/user/temporary/final-door-result')

        response_change_to_three = self.client.post(
            '/choose_final_door',
            {'door_chosen': 3}
        )

        self.assertEqual(response_change_to_three.status_code, 302)
        self.assertEqual(response_change_to_three['location'], '/user/temporary/final-door-result')

    def test_first_result_page_can_display_a_POST_request(self):
        self.login_temp()
        response_home = self.client.post(
            '/user/temporary/door_page_one', {'door_chosen': 1}
        )
        response_first_door_result = self.client.post(
            '/user/temporary/door-result/', {'door_chosen': 1}
        )
        request = HttpRequest()
        user = User.objects.get(username='temporary')
        response_final_door_result = final_door_result_page(
            request, user.username)
        html_final_door_result = response_final_door_result.content.decode(
            'utf8')
        self.assertIn("You chose door1", html_final_door_result)
