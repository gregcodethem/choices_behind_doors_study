from unittest import skip

from django.urls import resolve
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
        self.assertIn('Have another go at remembering the pattern',html)

    def test_prelim_three_continue_message_links_to_correct_page(self):
        self.login_temp()

        response = self.client.get(
            '/prelim_three',
            follow=True,
        )
        html = response.content.decode('utf8')

        self.assertIn('<a href="/prelim_three_part_b_feedback"', html)

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
