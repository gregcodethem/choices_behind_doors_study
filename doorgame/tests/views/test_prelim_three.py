from unittest import skip
from unittest.mock import patch

from django.urls import resolve

from doorgame.views import prelim_three
from doorgame.models import MemoryGame

from .base import BaseTest


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

    def test_prelim_three_part_b_feedback_POST_leads_to_correct_template(self):
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
            data=post_data,
        )
        self.assertTemplateUsed(response, 'prelim_three_part_b_feedback.html')

    def test_prelim_three_part_b_feedback_POST_inherits_from_correct_base_template(self):
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
            data=post_data,
        )
        self.assertTemplateUsed(response, 'prelim_three_part_b_feedback_base.html')

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

        self.assertIn(
            'box_1',
            response.content.decode()
        )


    @skip
    def test_post_request(self):
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

        # Send a POST request to the URL
        response = self.client.post(
            '/prelim_three_part_b_feedback',
            data=post_data
        )

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Optionally check that some expected data is in the response
        # self.assertContains(response, 'expected content')


class prelimThreeSecondGoTest(BaseTest):

    def test_prelim_three_second_go_returns_continue_message(self):
        self.login_temp()

        response = self.client.get(
            '/prelim_three_second_go',
            follow=True,
        )
        html = response.content.decode('utf8')

        self.assertIn('Continue to next page', html)

    def test_prelim_three_second_go_contains_link_to_correct_page(self):
        self.login_temp()

        response = self.client.get(
            '/prelim_three_second_go'
        )
        html = response.content.decode('utf8')

        self.assertIn('action="/prelim_three_part_b_feedback_second_go"', html)

    def test_prelim_three_part_b_feedback_second_go_POST_leads_to_correct_template(self):
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
            '/prelim_three_part_b_feedback_second_go',
            data=post_data,
        )
        self.assertTemplateUsed(response, 'prelim_three_part_b_feedback.html')


class PrelimThreeFourByFourTest(BaseTest):

    def test_prelim_three_four_by_four_user_sees_prelim_three_page(self):
        self.login_temp()

        self.set_to_four_by_four()

        response = self.client.get('/prelim_three', follow=True)

        html = response.content.decode('utf8')
        self.assertIn('Can you remember the pattern from before?', html)

    def test_prelim_three_returns_prelim_three_template(self):
        self.login_temp()

        self.set_to_four_by_four()

        response = self.client.get('/prelim_three', follow=True)
        self.assertTemplateUsed(response, 'prelim_three_four_by_four.html')

    def test_prelim_three_part_b_four_by_four_GET_request_returns_correct_template(self):
        self.login_temp()

        self.set_to_four_by_four()

        response = self.client.get('/prelim_three_part_b_feedback', follow=True)
        self.assertTemplateUsed(response, 'prelim_three_part_b_feedback_four_by_four.html')

    def test_prelim_three_part_b_four_by_four_POST_request_returns_correct_template(self):
        self.login_temp()

        self.set_to_four_by_four()

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
            'box_10': 'False',
            'box_11': 'False',
            'box_12': 'False',
            'box_13': 'False',
            'box_14': 'False',
            'box_15': 'False',
            'box_16': 'False',
        }

        response = self.client.post('/prelim_three_part_b_feedback', data=post_data)
        self.assertTemplateUsed(response, 'prelim_three_part_b_feedback_four_by_four.html')

    def test_prelim_three_part_b_four_by_four_POST_request_inherits_from_base_template(self):
        self.login_temp()

        self.set_to_four_by_four()

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
            'box_10': 'False',
            'box_11': 'False',
            'box_12': 'False',
            'box_13': 'False',
            'box_14': 'False',
            'box_15': 'False',
            'box_16': 'False',
        }

        response = self.client.post('/prelim_three_part_b_feedback', data=post_data)
        self.assertTemplateUsed(response, 'prelim_three_part_b_feedback_base.html')
