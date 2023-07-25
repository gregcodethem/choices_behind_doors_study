from django.urls import resolve

from doorgame.views import (
    home_page_user,
    consent_questions,
    prelim_one,
    prelim_one_part_b,
)

from doorgame.tests.views.base import BaseTest


class SimpleTestFirstPageLoggedIn(BaseTest):

    def test_user_url_resolves_to_home_page_user_view(self):
        self.login_temp()
        found = resolve('/user')
        self.assertEqual(found.func, home_page_user)


    def test_user_url_redirects_to_terms_and_conditions_url(self):
        self.login_temp()
        response = self.client.get('/user', follow=True)
        self.assertRedirects(response,'/prelim/terms_and_conditions')


    def test_home_page_user_sees_participation_information_sheet_first_page_on_login(self):
        self.login_temp()
        response = self.client.get('/user', follow=True)

        html = response.content.decode('utf8')
        self.assertIn('Participant Information Sheet', html)

    def test_home_page_returns_correct_template(self):
        self.login_temp()
        response = self.client.get('/user', follow=True)
        self.assertTemplateUsed(response, 'prelim/terms_and_conditions.html')

    def test_redirect_user_url(self):
        # Make a request that results in a redirect
        self.login_temp()
        response = self.client.get('/user', follow=True)

        # Check if there was a redirect
        if response.redirect_chain:
            # Get the final URL after all redirects
            final_url, status_code = response.redirect_chain[-1]

            # Now you can perform assertions on the final_url
            self.assertEqual(final_url, '/prelim/terms_and_conditions')
        else:
            self.fail('No redirect occurred')


class SimpleTestSecondPage(BaseTest):
    def test_consent_questions_url_resolves_to_consent_questions_view(self):
        self.login_temp()
        found = resolve('/prelim/consent_questions')
        self.assertEqual(found.func, consent_questions)

    def test_consent_questions_user_sees_consent_form(self):
        self.login_temp()
        response = self.client.get('/prelim/consent_questions', follow=True)

        html = response.content.decode('utf8')
        self.assertIn('CONSENT FORM', html)

    def test_consent_questions_returns_correct_template(self):
        self.login_temp()
        response = self.client.get('/prelim/consent_questions', follow=True)
        self.assertTemplateUsed(response, 'prelim/consent_questions.html')


class PrelimOneTest(BaseTest):
    def test_prelim_one_url_resolves_to_prelim_one_view(self):
        self.login_temp()
        found = resolve('/prelim_one')
        self.assertEqual(found.func, prelim_one)

    def test_prelim_one_user_sees_prelim_one_page(self):
        self.login_temp()
        response = self.client.get('/prelim_one', follow=True)

        html = response.content.decode('utf8')
        self.assertIn('Welcome to the Monty Hall Game under a memory task.', html)

    def test_prelim_one_returns_prelim_one_template(self):
        self.login_temp()
        response = self.client.get('/prelim_one', follow=True)
        self.assertTemplateUsed(response, 'prelim/prelim_one.html')


class PrelimOnePartBTest(BaseTest):
    def test_prelim_one_part_b_url_resolves_to_prelim_one_part_b_view(self):
        self.login_temp()
        found = resolve('/prelim_one_part_b')
        self.assertEqual(found.func, prelim_one_part_b)

    def test_prelim_one_part_b_user_sees_prelim_one_part_b_page(self):
        self.login_temp()
        response = self.client.get('/prelim_one_part_b', follow=True)

        html = response.content.decode('utf8')
        self.assertIn('You will see a matrix with randomly placed dots on it.', html)

    def test_prelim_one_part_b_returns_prelim_one_part_b_template(self):
        self.login_temp()
        response = self.client.get('/prelim_one_part_b', follow=True)
        self.assertTemplateUsed(response, 'prelim/prelim_one_part_b.html')
