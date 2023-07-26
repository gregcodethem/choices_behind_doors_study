from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings

from doorgame.models import SurveyAnswers

display_trial_limit = settings.TRIAL_LIMIT - 1
four_by_four_setting_list = ["very_hard", "medium", "very_easy"]
four_by_four_setting_list_two_options = ["medium", "very_easy"]

third_row_number_list = ['9', '10', '11', '12']
fourth_row_number_list = ['13', '14', '15', '16']
all_number_row_list = ['1', '2', '3', '4', '5', '6', '7',
                       '8', '9', '10', '11', '12', '13', '14', '15', '16']


def final_completion(request):
    return render(request, 'post_game/final_completion.html')


@login_required(login_url='accounts/login')
def final_survey_one(request):
    username_logged_in = request.user.username

    return render(request, 'post_game/final_survey_one.html',
                  {'display_trial_limit': display_trial_limit
                   })


@login_required(login_url='accounts/login')
def final_survey_one_completed(request):
    username_logged_in = request.user.username
    user = request.user
    if request.method == "POST":
        user_logged_in = request.user
        survey_answers_for_user = SurveyAnswers.objects.filter(
            user=user_logged_in
        )
        survey_answers = survey_answers_for_user.last()
        best_strategy = request.POST.get('best_strategy')
        survey_answers.best_strategy = best_strategy
        survey_answers.save()
        # changed the redirect page to final_survey_three.html
        # missing out the no longer needed final_survey_two.html
        return render(request,
                      'post_game/final_survey_three.html', {
                          "username": username_logged_in,
                          "display_trial_limit": display_trial_limit,
                      })


def final_survey_two_completed(request):
    if request.method == "POST":
        user_logged_in = request.user
        survey_answers_for_user = SurveyAnswers.objects.filter(
            user=user_logged_in
        )
        survey_answers = survey_answers_for_user.last()
        estimate_stayed_lost = request.POST.get('stayed-lost')
        estimate_stayed_won = request.POST.get('stayed-won')
        estimate_switched_lost = request.POST.get('switched-lost')
        estimate_switched_won = request.POST.get('switched-lost')

        survey_answers.estimate_stayed_lost = estimate_stayed_lost
        survey_answers.estimate_stayed_won = estimate_stayed_won
        survey_answers.estimate_switched_lost = estimate_switched_lost
        survey_answers.estimate_stayed_won = estimate_switched_won

        survey_answers.save()

        return render(request,
                      'post_game/final_survey_three.html')


def final_survey_three_completed(request):
    if request.method == "POST":
        user_logged_in = request.user
        username_logged_in = user_logged_in.username
        survey_answers_for_user = SurveyAnswers.objects.filter(
            user=user_logged_in
        )
        survey_answers = survey_answers_for_user.last()

        familiar = request.POST.get('familiar')
        survey_answers.familiar = familiar

        english = request.POST.get('english')
        survey_answers.english = english

        age = request.POST.get('age')
        survey_answers.age = age

        gender = request.POST.get('gender')
        survey_answers.gender = gender
        education_level = request.POST.get('education_level')
        survey_answers.education_level = education_level
        survey_answers.save()

        return render(request, 'post_game/thankyou.html', {
            'username': username_logged_in
        })
