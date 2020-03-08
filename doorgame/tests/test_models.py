from django.test import TestCase

from doorgame.models import Choice
from django.contrib.auth.models import User


class ChoiceModelTest(TestCase):

    def test_saving_and_retrieving_choices(self):
        user_test = User.objects.create_user(
            'george',
            '',
            'somethingpassword')
        user_test.save()
        first_choice = Choice()
        first_choice.door_number = 1
        first_choice.user = user_test
        first_choice.save()

        second_choice = Choice()
        second_choice.door_number = 2
        second_choice.user = user_test
        second_choice.save()

        saved_choices = Choice.objects.all()
        self.assertEqual(saved_choices.count(), 2)

        first_saved_choice = saved_choices[0]
        second_saved_choice = saved_choices[1]
        self.assertEqual(first_saved_choice.door_number, 1)
        self.assertEqual(second_saved_choice.door_number, 2)

    def test_saving_and_retrieving_user_name_from_choices(self):
        user_test_one = User.objects.create_user(
            'george',
            '',
            'somethingpassword')
        user_test_one.save()
        first_choice = Choice()
        first_choice.door_number = 1
        first_choice.user = user_test_one
        first_choice.save()

        user_test_two = User.objects.create_user(
            'brian',
            '',
            'not-the-messiah')
        user_test_two.save()
        second_choice = Choice()
        second_choice.door_number = 2
        second_choice.user = user_test_two
        second_choice.save()

        saved_choices = Choice.objects.all()
        self.assertEqual(saved_choices.count(), 2)

        first_saved_choice = saved_choices[0]
        first_saved_user = first_saved_choice.user
        second_saved_choice = saved_choices[1]
        second_saved_user = second_saved_choice.user
        self.assertEqual(first_saved_user, user_test_one)
        self.assertEqual(second_saved_user, user_test_two)
