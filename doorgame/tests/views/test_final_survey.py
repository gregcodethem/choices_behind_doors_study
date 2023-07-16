from .base import BaseTest

class FinalSurveyOneTest(BaseTest):

    def test_final_survey_one_link_to_correct_template(self):
        self.login_temp()

        response = self.client.get('/final_survey_one')

        self.assertTemplateUsed(response, 'final_survey_one.html')

    def test_final_survey_one_saves_models(self):

        self.login_temp()

