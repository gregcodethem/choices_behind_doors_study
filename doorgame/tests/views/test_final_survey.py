from django.contrib.auth.models import User

from .base import BaseTest
from doorgame.models import SurveyAnswers

class FinalSurveyOneTest(BaseTest):

    def test_final_survey_one_link_to_correct_template(self):
        self.login_temp()

        response = self.client.get('/final_survey_one')

        self.assertTemplateUsed(response, 'final_survey_one.html')

    def test_final_survey_one_saves_models(self):

        self.login_temp()
        user = User.objects.get(username='temporary')
        SurveyAnswers.objects.create(user=user)

        response = self.client.post(
            '/final_survey_one_completed',
            {'best_strategy': 'stick'}
        )

        user = User.objects.get(username='temporary')
        survey_answers_all = SurveyAnswers.objects.filter(user=user)
        survey_answers = survey_answers_all.last()
        saved_best_strategy = survey_answers.best_strategy

        self.assertEqual(len(survey_answers_all), 1)
        self.assertEqual(saved_best_strategy,'stick')

    def test_final_survey_one_completed_links_to_correct_template(self):
        self.login_temp()
        user = User.objects.get(username='temporary')
        SurveyAnswers.objects.create(user=user)

        response = self.client.post(
            '/final_survey_one_completed',
            {'best_strategy': 'stick'}
        )

        self.assertTemplateUsed(response, 'final_survey_three.html')

    def test_final_survey_three_saves_models(self):

        self.login_temp()
        user = User.objects.get(username='temporary')
        SurveyAnswers.objects.create(user=user)

        response = self.client.post(
            '/final_survey_three_completed',
            {'familiar': 'yes',
             'english': 'no',
             'age': '33',
             'gender': 'male',
             'education_level': 'master'}
        )

        user = User.objects.get(username='temporary')
        survey_answers_all = SurveyAnswers.objects.filter(user=user)
        survey_answers = survey_answers_all.last()
        saved_familar_with_game = survey_answers.familiar
        saved_english_native_language = survey_answers.english
        saved_age = survey_answers.age
        saved_gender = survey_answers.gender
        saved_education_level = survey_answers.education_level

        self.assertEqual(len(survey_answers_all), 1)
        self.assertEqual(saved_familar_with_game,'yes')
        self.assertEqual(saved_english_native_language,'no')
        self.assertEqual(saved_age, 33)
        self.assertEqual(saved_gender, 'male')
        self.assertEqual(saved_education_level, 'master')

    def test_final_survey_three_completed_links_to_correct_template(self):
        self.login_temp()
        user = User.objects.get(username='temporary')
        SurveyAnswers.objects.create(user=user)

        response = self.client.post(
            '/final_survey_three_completed',
            {'familiar': 'yes',
             'english': 'no',
             'age': '33',
             'gender': 'male',
             'education_level': 'master'}
        )

        self.assertTemplateUsed(response, 'thankyou.html')