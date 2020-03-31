from random import randint
# changed name of random.choice so as not to confuse with
# the choice model instance
from random import choice as randomchoice

from django.shortcuts import render, redirect
from django.http import HttpResponse
from doorgame.models import Choice, Trial, Result, MemoryGame, SurveyAnswers
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

# Create your views here.

trial_limit = 60

def home_page(request, user=None):
    return redirect('/user')


@login_required(login_url='accounts/login')
def final_pattern(request):
    username_logged_in = request.user.username
    if request.method == 'POST':
        memory_game = MemoryGame()
        # if I can retrieve anything then the request should be true
        # if not then it should be false
        user_logged_in = request.user
        username_logged_in = user_logged_in.username

        # find the trials by this user
        trial_existing_objects = Trial.objects.filter(
            user=request.user
        )
        trial_existing = trial_existing_objects.last()
        memory_game.trial = trial_existing
        # if I can retrieve anything then the request should be true
        # if not then it should be false

        if request.POST.get('box_1') == "True":
            memory_game.box_1 = True
        if request.POST.get('box_2') == "True":
            memory_game.box_2 = True
        memory_game.initial_or_final = 'final'
        memory_game.save()


        trial_number = trial_existing.number_of_trial
        if trial_number >= trial_limit:
            return redirect('/user/' + username_logged_in + '/final_survey_one')

        return redirect('/user/' + username_logged_in)

    else:
        print("final_pattern_step has NOT registered post request")
    return redirect('/user/' + username_logged_in)


@login_required(login_url='accounts/login')
def home_page_user(request):
    username_logged_in = request.user.username
    if username_logged_in:
        return redirect('/user/' + username_logged_in)

    else:
        return render(request, 'home.html')


@login_required(login_url='accounts/login')
def choose_door(request):
    username_logged_in = request.user.username
    if request.method == 'POST':
        user_logged_in = request.user

        # Here I need to retrieve the latest trial
        # find the trials by this user
        trial_existing_objects = Trial.objects.filter(
            user=request.user
        )
        trial_existing = trial_existing_objects.last()

        choice = Choice()
        choice.door_number = request.POST.get('door_chosen', 0)
        choice.trial = trial_existing
        choice.save()

        result = Result()
        result.door_number = randint(1, 3)
        result.trial = trial_existing
        result.save()

        return redirect('/user/' + username_logged_in + '/door-result')
    else:
        pass


@login_required(login_url='accounts/login')
def choose_final_door(request):
    if request.method == 'POST':
        user_logged_in = request.user
        username_logged_in = user_logged_in.username

        # find the trials by this user
        trial_existing_objects = Trial.objects.filter(
            user=request.user
        )
        trial_existing = trial_existing_objects.last()
        choice = Choice()
        choice.door_number = request.POST.get('final_door_chosen', 0)
        choice.trial = trial_existing
        choice.first_or_second_choice = 2
        choice.save()

        return redirect('/user/' + username_logged_in + '/final-door-result')


@login_required(login_url='accounts/login')
def home_page_memory_game(request, username):
    username_logged_in = request.user.username
    user_logged_in = request.user


    if request.method == 'POST':
        # insert method to remember pattern here (if necessary)
        return redirect('/user/' + username_logged_in + '/door-page-one')

    else:



        trial = Trial()
        trial.user = request.user

        trials_for_this_user = Trial.objects.filter(user=user_logged_in)
        latest_trial = trials_for_this_user.last()
        if len(trials_for_this_user) != 0:
            number_of_trial = latest_trial.number_of_trial + 1
        else:
            number_of_trial = 1
        trial.number_of_trial = number_of_trial
        trial.save()
        # insert some method here to generate the pattern
        memory_game = MemoryGame()
        memory_game.box_1 = True
        memory_game.box_2 = False 
        memory_game.trial = trial
        memory_game.save()

    return render(request, 'home.html', {
        "username": username_logged_in,
        "number_of_trial": number_of_trial,
        "memory_game": memory_game,
    })


@login_required(login_url='accounts/login')
def door_page_one(request):
    username_logged_in = request.user.username

    if request.method == "POST":
        return redirect('/user/' + username_logged_in + '/door_page_one')
    return redirect('/user/' + username_logged_in + '/door_page_one')


@login_required(login_url='accounts/login')
def home_page_user_unique(request, username):
    username_logged_in = request.user.username
    user_logged_in = request.user

    if request.method == 'POST':
        choose_door(request)
        return redirect('/user/' + username_logged_in + '/door-result')

    return render(request,
                  'door-page-one.html', {
                      "username": username_logged_in,
                  })


def door_result_page(request, username):
    if request.method == "POST":
        user_logged_in = request.user
        username_logged_in = user_logged_in.username
        choose_final_door(request)
        return redirect('/user/' + username_logged_in + '/final-door-result')
    choice = Choice.objects.last()
    if choice:
        chosen_number = choice.door_number
        possible_numbers = [1, 2, 3]
        possible_numbers.remove(chosen_number)
        trial = choice.trial
        result = Result.objects.get(trial=trial)
        result_number = result.door_number
        try:
            possible_numbers.remove(result_number)
        except ValueError:
            pass
        # We should be left with either one or two numbers left
        if len(possible_numbers) == 1:
            number_to_remove = possible_numbers[0]
        elif len(possible_numbers) == 2:
            # fi there's a choice of 2 numbers to remove,
            # in this case they've already chosen the right number,
            # then remove at random one of the remaining 2 numbers.
            number_to_remove = randomchoice(possible_numbers)
        other_door_choice_list = [1, 2, 3]
        other_door_choice_list.remove(chosen_number)
        other_door_choice_list.remove(number_to_remove)
        number_to_change_to = other_door_choice_list[0]

        return render(request, 'door_result.html', {
            'door_chosen_number': str(choice.door_number),
            'door_to_remove_number': str(number_to_remove),
            'door_to_change_to_number': str(number_to_change_to),
        })
    else:
        return render(request, 'door_result.html',
                      )


def final_door_result_page(request, username):
    choice = Choice.objects.last()
    if choice:
        final_chosen_number = choice.door_number

        return render(request, 'final_door_result.html', {
            'final_door_chosen_number': str(final_chosen_number)
        })
    else:
        return render(request, 'final_door_result.html')

@login_required(login_url='accounts/login')
def final_survey_one(request, username):
    username_logged_in = request.user.username

    return render(request, 'final_survey_one.html',)

@login_required(login_url='accounts/login')
def final_survey_one_completed(request):
    username_logged_in = request.user.username
    user = request.user
    if request.method =="POST":
        survey_answers = SurveyAnswers()
        survey_answers.user = user
        best_strategy = request.POST.get('best_strategy')
        survey_answers.best_strategy = best_strategy
        survey_answers.save()
        return render (request,
                  'final_survey_two.html', {
                      "username": username_logged_in,
                  })


def final_survey_two_completed(request):
    if request.method == "POST":
        user = request.user
        survey_answers = SurveyAnswers()
        survey_answers.user = user
        estimate_stayed_lost = request.POST.get('stayed-lost')
        estimate_stayed_won = request.POST.get('stayed-won')
        estimate_switched_lost = request.POST.get('switched-lost')
        estimate_switched_won = request.POST.get('switched-lost')
        
        survey_answers.estimate_stayed_lost = estimate_stayed_lost
        survey_answers.estimate_stayed_won = estimate_stayed_won
        survey_answers.estimate_switched_lost = estimate_switched_lost
        survey_answers.estimate_stayed_won = estimate_switched_won
        
        familiar = request.POST.get('familiar')
        survey_answers.familiar = familiar
        age = request.POST.get('age')
        survey_answers.age = age

        gender = request.POST.get('gender')
        survey_answers.gender = 'male'
        education_level = request.POST.get('education-level')
        survey_answers.education_level = education_level
        survey_answers.save()

        return render(request, 'thankyou.html')

def final_survey_three_completed(request):
    pass
