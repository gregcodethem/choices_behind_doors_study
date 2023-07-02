from unittest import skip

from django.urls import (
    resolve,
    reverse,
)
from django.test import Client
from django.http import HttpRequest


from doorgame.views import (
    home_page,
    home_page_user,
    home_page_user_unique,
    consent_questions,
    prelim_one,
    prelim_one_part_b,
    prelim_two,
    prelim_three,
)

from doorgame.models import Choice, Trial, Result, MemoryGame, Profile
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from .base import BaseTest


class PrelimTwoTest(BaseTest):
    def test_prelim_two_url_resolves_to_prelim_two_view(self):
        self.login_temp()
        found = resolve('/prelim_two')
        self.assertEqual(found.func, prelim_two)

    def test_prelim_two_user_sees_prelim_two_page(self):
        self.login_temp()

        response = self.client.get('/prelim_two', follow=True)

        html = response.content.decode('utf8')
        self.assertIn('<div class="row no-gutters">', html)

    def test_prelim_two_returns_prelim_two_template(self):
        self.login_temp()

        response = self.client.get('/prelim_two', follow=True)
        self.assertTemplateUsed(response, 'prelim_two.html')


class PrelimTwoFourByFourTest(BaseTest):

    def test_prelim_two_four_by_four_user_sees_prelim_two_four_by_four_page(self):
        self.login_temp()

        # Get the user
        user = User.objects.get(username='temporary')

        # Get or create the profile associated with the user
        profile, created = Profile.objects.get_or_create(user=user)

        # Update the profile fields
        profile.hard_or_easy_dots = ""  # Reassigned as its default
        profile.low_medium_or_high_dots_setting = "very_easy"

        # Save the updated profile
        profile.save()

        response = self.client.get('/prelim_two', follow=True)

        html = response.content.decode('utf8')
        self.assertIn('<div class="row no-gutters">', html)

    def test_prelim_two_four_by_four_returns_prelim_two_four_by_four_template(self):
        self.login_temp()

        # Get the user
        user = User.objects.get(username='temporary')

        # Get or create the profile associated with the user
        profile, created = Profile.objects.get_or_create(user=user)

        # Update the profile fields
        profile.hard_or_easy_dots = ""  # Reassigned as its default
        profile.low_medium_or_high_dots_setting = "very_easy"

        # Save the updated profile
        profile.save()

        response = self.client.get('/prelim_two', follow=True)
        self.assertTemplateUsed(response, 'prelim_two_four_by_four.html')


class PrelimThreeTest(BaseTest):
    def test_prelim_three_url_resolves_to_prelim_three_view(self):
        self.login_temp()
        found = resolve('/prelim_three')
        self.assertEqual(found.func, prelim_three)

    def test_prelim_three_user_sees_prelim_three_page(self):
        self.login_temp()

        response = self.client.get('/prelim_three', follow=True)

        html = response.content.decode('utf8')
        self.assertIn('Can you remember the pattern from before?', html)

    def test_prelim_three_returns_prelim_three_template(self):
        self.login_temp()

        response = self.client.get('/prelim_three', follow=True)
        self.assertTemplateUsed(response, 'prelim_three.html')

    def test_prelim_three_returns_continue_message(self):
        self.login_temp()

        response = self.client.get(
            '/prelim_three',
            follow=True,
        )
        html = response.content.decode('utf8')

        # test desired continue message is displayed:
        self.assertIn('Continue to next page',html)

    # javascript introduced has broken following test,
    # update or remove
    def test_prelim_three_contains_links_to_correct_page(self):
        self.login_temp()

        response = self.client.get(
            '/prelim_three',
            follow=True,
        )
        html = response.content.decode('utf8')

        self.assertIn('action="/prelim_three_part_b_feedback"', html)

    def test_prelim_three_part_b_feedback_leads_to_correct_template(self):
        # !!!!! Look at again!!!
        # Not sure if in the right format
        # This is testing a get request
        # which should not be called
        self.login_temp()

        response = self.client.get(
            '/prelim_three_part_b_feedback',
            follow=True,
        )
        self.assertTemplateUsed(response, 'prelim_three_part_b_feedback.html')

    def test_prelim_three_link_returns_post_request(self):
        pass

    def test_can_save_a_POST_request(self):
        self.login_temp()
        # Simulate POST data
        post_data = {
            'box_1': 'True',
            'box_2': 'True',
            'box_3': 'True',
            'box_4': 'False',
            'box_5': 'False',
            'box_6': 'False',
            'box_7': 'False',
            'box_8': 'False',
            'box_9': 'False',
        }

        response = self.client.post(
            '/prelim_three_part_b_feedback',
            data=post_data
        )
        '''self.assertIn(
            'True',
            response.content.decode()
        )'''
        self.assertIn(
            'box_1',
            response.content.decode()
        )



    def test_post_request(self):
        # Simulate POST data
        post_data = {
            'box_1': 'True',
            'box_2': 'True',
            # ... other data ...
        }

        # Send a POST request to the URL
        response = self.client.post(reverse('prelim_three_part_b_feedback'), data=post_data)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Optionally check that some expected data is in the response
        # self.assertContains(response, 'expected content')


class prelimThreeSecondGoTest(BaseTest):

    def test_prelim_three_second_go_returns_continue_message(self):
        self.login_temp()

        response = self.client.get(
            '/prelim_three_second_go'
        )
        html = response.content.decode('utf8')

        self.assertIn('Go to next page', html)

    def test_prelim_three_second_go_returns_correct_link(self):
        self.login_temp()

        response = self.client.get(
            '/prelim_three_second_go'
        )
        html = response.content.decode('utf8')

        self.assertIn('<a href="/prelim_three_part_b_feedback_second_go"', html)


class PrelimThreeFourByFourTest(BaseTest):

    def test_prelim_three_four_by_four_user_sees_prelim_three_page(self):
        self.login_temp()

        # Get the user
        user = User.objects.get(username='temporary')

        # Get or create the profile associated with the user
        profile, created = Profile.objects.get_or_create(user=user)

        # Update the profile fields
        profile.hard_or_easy_dots = ""  # Reassigned as its default
        profile.low_medium_or_high_dots_setting = "very_easy"

        # Save the updated profile
        profile.save()

        response = self.client.get('/prelim_three', follow=True)

        html = response.content.decode('utf8')
        self.assertIn('Can you remember the pattern from before?', html)

    def test_prelim_three_returns_prelim_three_template(self):
        self.login_temp()

        # Get the user
        user = User.objects.get(username='temporary')

        # Get or create the profile associated with the user
        profile, created = Profile.objects.get_or_create(user=user)

        # Update the profile fields
        profile.hard_or_easy_dots = ""  # Reassigned as its default
        profile.low_medium_or_high_dots_setting = "very_easy"

        # Save the updated profile
        profile.save()

        response = self.client.get('/prelim_three', follow=True)
        self.assertTemplateUsed(response, 'prelim_three_four_by_four.html')
