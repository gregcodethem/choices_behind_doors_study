from random import randint
# changed name of random.choice so as not to confuse with
# the choice model instance
from random import choice as randomchoice

from django.shortcuts import render, redirect
from django.http import HttpResponse
from doorgame.models import Choice, Trial, Result, MemoryGame, SurveyAnswers, MemoryGameList
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from .utils import memory_game_bool_matrix, add_memory_games
from .all_dots import all_dots_list
# Create your views here.

from config.settings import TRIAL_LIMIT


def final_completion(request):
    return render(request, 'final_completion.html')


def home_page(request, user=None):
    return redirect('/user')


@login_required(login_url='accounts/login')
def remember_memory_game(request):
    return render(request, 'remember_memory_game.html')


@login_required(login_url='accounts/login')
def final_pattern(request):
    username_logged_in=request.user.username
    if request.method == 'POST':
        memory_game=MemoryGame()
        # if I can retrieve anything then the request should be true
        # if not then it should be false
        user_logged_in=request.user
        username_logged_in=user_logged_in.username

        # find the trials by this user
        trial_existing_objects=Trial.objects.filter(
            user=request.user
        )
        trial_existing=trial_existing_objects.last()
        memory_game.trial=trial_existing
        # if I can retrieve anything then the request should be true
        # if not then it should be false

        if request.POST.get('box_1') == "True":
            memory_game.box_1=True
        if request.POST.get('box_2') == "True":
            memory_game.box_2=True
        if request.POST.get('box_3') == "True":
            memory_game.box_3 == True
        if request.POST.get('box_4') == "True":
            memory_game.box_4 == True
        if request.POST.get('box_5') == "True":
            memory_game.box_5=True
        if request.POST.get('box_6') == "True":
            memory_game.box_6=True
        if request.POST.get('box_7') == "True":
            memory_game.box_7 == True
        if request.POST.get('box_8') == "True":
            memory_game.box_8 == True
        if request.POST.get('box_9') == "True":
            memory_game.box_9=True

        memory_game.initial_or_final='final'
        memory_game.save()

        trial_number=trial_existing.number_of_trial
        if trial_number >= TRIAL_LIMIT - 1:
            return redirect('/user/' + username_logged_in + '/final_survey_one')

        return redirect('/trial_completed')

    else:
        print("final_pattern_step has NOT registered post request")
    return redirect('/user/' + username_logged_in)


@login_required(login_url='accounts/login')
def trial_completed(request):
    user=request.user
    trial_existing_objects=Trial.objects.filter(
        user=request.user
    )
    trial_existing=trial_existing_objects.last()
    number_of_trial=trial_existing.number_of_trial
    return render(request, 'trial_completed.html',
                  {'trial_number': number_of_trial
                   })


@login_required(login_url='accounts/login')
def home_page_user(request):
    username_logged_in=request.user.username
    if username_logged_in:
        return redirect('/user/' + username_logged_in)

    else:
        return render(request, 'home.html')


@login_required(login_url='accounts/login')
def choose_door(request):
    username_logged_in=request.user.username
    if request.method == 'POST':
        user_logged_in=request.user

        # Here I need to retrieve the latest trial
        # find the trials by this user
        trial_existing_objects=Trial.objects.filter(
            user=request.user
        )
        trial_existing=trial_existing_objects.last()

        choice=Choice()
        choice.door_number=request.POST.get('door_chosen', 0)
        choice.trial=trial_existing
        choice.save()

        result=Result()
        result.door_number=randint(1, 3)
        result.trial=trial_existing
        result.save()

        return redirect('/user/' + username_logged_in + '/door-result')
    else:
        pass


@login_required(login_url='accounts/login')
def choose_final_door(request):
    if request.method == 'POST':
        user_logged_in=request.user
        username_logged_in=user_logged_in.username

        # find the trials by this user
        trial_existing_objects=Trial.objects.filter(
            user=request.user
        )
        trial_existing=trial_existing_objects.last()
        choice=Choice()
        choice.door_number=request.POST.get('final_door_chosen', 0)
        choice.trial=trial_existing
        choice.first_or_second_choice=2
        choice.save()

        return redirect('/user/' + username_logged_in + '/final-door-result')


@login_required(login_url='accounts/login')
def home_page_memory_game(request, username):
    # logout_if_reached_the_limit(request)
    user_logged_in=request.user
    trials_for_this_user=Trial.objects.filter(user=user_logged_in)
    if len(trials_for_this_user) != 0:
        latest_trial=trials_for_this_user.last()

        if latest_trial.number_of_trial >= TRIAL_LIMIT:
            return final_completion(request)

        else:
            pass


    username_logged_in=request.user.username
    user_logged_in=request.user

    if request.method == 'POST':
        # insert method to remember pattern here (if necessary)
        return redirect('/user/' + username_logged_in + '/door-page-one')

    else:

        memory_game_list_prelim=MemoryGameList.objects.filter(
            user=user_logged_in)
        print(f'first instance of memory game list {memory_game_list_prelim}')
        if len(memory_game_list_prelim) == 0:
            print('len of memory game list was 0, so creating new memory_game_list model')
            memory_game_list=MemoryGameList()
            memory_game_list.user=user_logged_in
            memory_game_list.save()
            add_memory_games(memory_game_list)
            memory_game_list=[memory_game_list]
        else:
            memory_game_list=memory_game_list_prelim

        trial=Trial()
        trial.user=request.user

        trials_for_this_user=Trial.objects.filter(user=user_logged_in)
        latest_trial=trials_for_this_user.last()
        if len(trials_for_this_user) != 0:
            number_of_trial=latest_trial.number_of_trial + 1
        else:
            number_of_trial=0
        trial.number_of_trial=number_of_trial
        trial.save()

        # !!!!!----- This is the bit I need to change so
        # that it's seeing the different patterns
        # insert some method here to generate the pattern

        
        if len(memory_game_list) != 0:
            memory_game_list_end=MemoryGame.objects.filter(
                memory_game_list=memory_game_list[0],
                number_of_trial=number_of_trial
            )
            memory_game=memory_game_list_end[0]
            memory_game.trial=trial
            memory_game.save()

    if number_of_trial == 0:
        return render(request, 'prelim_one.html', {
            "username": username_logged_in,
            "number_of_trial": number_of_trial,
            "memory_game": memory_game,
        }
        )
    return render(request, 'home.html', {
        "username": username_logged_in,
        "number_of_trial": number_of_trial,
        "memory_game": memory_game,
    })


@login_required(login_url='accounts/login')
def prelim_two(request):
    class MemoryGamePrelimClass:
        pass
    MemoryGamePrelim=MemoryGamePrelimClass()
    MemoryGamePrelim.box_1=True
    MemoryGamePrelim.box_2=False
    MemoryGamePrelim.box_3=False
    MemoryGamePrelim.box_4=True
    MemoryGamePrelim.box_5=True
    MemoryGamePrelim.box_6=False
    MemoryGamePrelim.box_7=False
    MemoryGamePrelim.box_8=True
    MemoryGamePrelim.box_9=False
    return render(request, 'prelim_two.html', {
        "memory_game": MemoryGamePrelim,
        "first_go": True
    })


@login_required(login_url='accounts/login')
def prelim_two_second_go(request):
    class MemoryGamePrelimClass:
        pass
    MemoryGamePrelim=MemoryGamePrelimClass()
    MemoryGamePrelim.box_1=True
    MemoryGamePrelim.box_2=False
    MemoryGamePrelim.box_3=True
    MemoryGamePrelim.box_4=False
    MemoryGamePrelim.box_5=True
    MemoryGamePrelim.box_6=False
    MemoryGamePrelim.box_7=False
    MemoryGamePrelim.box_8=False
    MemoryGamePrelim.box_9=True
    return render(request, 'prelim_two.html', {
        "memory_game": MemoryGamePrelim,
        "first_go": False
    })


def prelim_three(request):
    return render(request, 'prelim_three.html',
                  {'repeat_example': True
                   })


def prelim_three_second_go(request):
    return render(request, 'prelim_three.html',
                  {'repeat_example': False
                   })


def prelim_four(request):
    return render(request, 'prelim_four.html')


@login_required(login_url='accounts/login')
def door_page_one(request):
    username_logged_in=request.user.username

    if request.method == "POST":
        return redirect('/user/' + username_logged_in + '/door_page_one')
    return redirect('/user/' + username_logged_in + '/door_page_one')


@login_required(login_url='accounts/login')
def home_page_user_unique(request, username):
    username_logged_in=request.user.username
    user_logged_in=request.user

    if request.method == 'POST':
        choose_door(request)
        return redirect('/user/' + username_logged_in + '/door-result')

    return render(request,
                  'door-page-one.html', {
                      "username": username_logged_in,
                  })

@login_required(login_url='accounts/login')
def door_result_page(request, username):
    if request.method == "POST":
        user_logged_in=request.user
        username_logged_in=user_logged_in.username
        choose_final_door(request)
        return redirect('/user/' + username_logged_in + '/final-door-result')
    # !----- Need to make choice specific to the user ----!

    # find the trials by this user
    trial_existing_objects=Trial.objects.filter(
        user=request.user
    )
    trial_existing=trial_existing_objects.last()
    choices_from_this_trial=Choice.objects.filter(
        trial=trial_existing
    )
    choice=choices_from_this_trial.last()
    if choice:
        chosen_number=choice.door_number
        possible_numbers=[1, 2, 3]
        possible_numbers.remove(chosen_number)
        trial=choice.trial
        result=Result.objects.get(trial=trial)
        result_number=result.door_number
        try:
            possible_numbers.remove(result_number)
        except ValueError:
            pass
        # We should be left with either one or two numbers left
        if len(possible_numbers) == 1:
            number_to_remove=possible_numbers[0]
        elif len(possible_numbers) == 2:
            # if there's a choice of 2 numbers to remove,
            # in this case they've already chosen the right number,
            # then remove at random one of the remaining 2 numbers.
            number_to_remove=randomchoice(possible_numbers)
        other_door_choice_list=[1, 2, 3]
        other_door_choice_list.remove(chosen_number)
        other_door_choice_list.remove(number_to_remove)
        number_to_change_to=other_door_choice_list[0]

        doors_to_display_list=[chosen_number,
                                 number_to_change_to
                                 ]
        if 1 in doors_to_display_list:
            door_one_bool=True
        else:
            door_one_bool=False
        if 2 in doors_to_display_list:
            door_two_bool=True
        else:
            door_two_bool=False
        if 3 in doors_to_display_list:
            door_three_bool=True
        else:
            door_three_bool=False

        return render(request, 'door_result.html', {
            'door_chosen_number': str(choice.door_number),
            'door_to_remove_number': str(number_to_remove),
            'door_to_change_to_number': str(number_to_change_to),
            'door_one_bool': door_one_bool,
            'door_two_bool': door_two_bool,
            'door_three_bool': door_three_bool,
        })
    else:
        return render(request, 'door_result.html',
                      )


def final_door_result_page(request, username):
    # find the trials by this user
    trial_existing_objects=Trial.objects.filter(
        user=request.user
    )
    trial_existing=trial_existing_objects.last()
    choices_from_this_trial=Choice.objects.filter(
        trial=trial_existing
    )
    choice=choices_from_this_trial.last()
    if choice:
        final_chosen_number=choice.door_number
        trial=choice.trial
        result=Result.objects.get(trial=trial)
        result_number=result.door_number
        if final_chosen_number == result_number:
            sucessfully_chose_right_door=True
        else:
            sucessfully_chose_right_door=False
        if 1 == result_number:
            door_one_bool=True
        else:
            door_one_bool=False
        if 2 == result_number:
            door_two_bool=True
        else:
            door_two_bool=False
        if 3 == result_number:
            door_three_bool=True
        else:
            door_three_bool=False

        return render(request, 'final_door_result.html', {
            'final_door_chosen_number': str(final_chosen_number),
            'sucessfully_chose_right_door': sucessfully_chose_right_door,
            'door_one_bool': door_one_bool,
            'door_two_bool': door_two_bool,
            'door_three_bool': door_three_bool,
        })
    else:
        return render(request, 'final_door_result.html')


@login_required(login_url='accounts/login')
def final_survey_one(request, username):
    username_logged_in=request.user.username

    return render(request, 'final_survey_one.html',)


@login_required(login_url='accounts/login')
def final_survey_one_completed(request):
    username_logged_in=request.user.username
    user=request.user
    if request.method == "POST":
        survey_answers=SurveyAnswers()
        survey_answers.user=user
        best_strategy=request.POST.get('best_strategy')
        survey_answers.best_strategy=best_strategy
        survey_answers.save()
        return render(request,
                      'final_survey_two.html', {
                          "username": username_logged_in,
                      })


def final_survey_two_completed(request):
    if request.method == "POST":
        user_logged_in=request.user
        survey_answers_for_user=SurveyAnswers.objects.filter(
            user=user_logged_in
        )
        survey_answers=survey_answers_for_user.last()
        estimate_stayed_lost=request.POST.get('stayed-lost')
        estimate_stayed_won=request.POST.get('stayed-won')
        estimate_switched_lost=request.POST.get('switched-lost')
        estimate_switched_won=request.POST.get('switched-lost')

        survey_answers.estimate_stayed_lost=estimate_stayed_lost
        survey_answers.estimate_stayed_won=estimate_stayed_won
        survey_answers.estimate_switched_lost=estimate_switched_lost
        survey_answers.estimate_stayed_won=estimate_switched_won

        survey_answers.save()

        return render(request,
                      'final_survey_three.html')


def final_survey_three_completed(request):
    if request.method == "POST":
        user_logged_in=request.user
        survey_answers_for_user=SurveyAnswers.objects.filter(
            user=user_logged_in
        )
        survey_answers=survey_answers_for_user.last()

        familiar=request.POST.get('familiar')
        survey_answers.familiar=familiar
        age=request.POST.get('age')
        survey_answers.age=age

        gender=request.POST.get('gender')
        survey_answers.gender=gender
        education_level=request.POST.get('education_level')
        survey_answers.education_level=education_level
        survey_answers.save()

        return render(request, 'thankyou.html')
