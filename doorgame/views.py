from random import randint
# changed name of random.choice so as not to confuse with
# the choice model instance
from random import choice as randomchoice
from secrets import choice as secretschoice
from string import ascii_letters, digits

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import (
    authenticate,
    login
)
from django.contrib.auth.models import User
from django.conf import settings

from doorgame.models import (
    Choice,
    Trial,
    Result,
    SurveyAnswers,
    Profile
)

display_trial_limit = settings.TRIAL_LIMIT - 1
four_by_four_setting_list = ["very_hard", "medium", "very_easy"]
four_by_four_setting_list_two_options = ["medium", "very_easy"]

def site_maintenance(request):
    return HttpResponse('<html><title>Site under maintenance</title><h1>Site under maintenance, we will be back online soon</h1></html>')


def home_page(request, user=None):
    return redirect('/user')


@login_required(login_url='accounts/login')
def outcome_of_doorgame(request):
    # find the trials by this user
    trial_existing_objects = Trial.objects.filter(
        user=request.user
    )
    trial_existing = trial_existing_objects.last()

    choices_from_this_trial = Choice.objects.filter(
        trial=trial_existing
    )
    choice = choices_from_this_trial.last()
    if choice:
        final_chosen_number = choice.door_number
        trial = choice.trial
        result = Result.objects.get(trial=trial)
        result_number = result.door_number
        if final_chosen_number == result_number:
            sucessfully_chose_right_door = True
        else:
            sucessfully_chose_right_door = False
        if 1 == result_number:
            door_one_bool = True
        else:
            door_one_bool = False
        if 2 == result_number:
            door_two_bool = True
        else:
            door_two_bool = False
        if 3 == result_number:
            door_three_bool = True
        else:
            door_three_bool = False

        return render(request, 'doorgame/final_door_result.html', {
            'final_door_chosen_number': str(final_chosen_number),
            'sucessfully_chose_right_door': sucessfully_chose_right_door,
            'door_one_bool': door_one_bool,
            'door_two_bool': door_two_bool,
            'door_three_bool': door_three_bool,
        })
    else:
        return render(request, 'doorgame/final_door_result.html')


@login_required(login_url='accounts/login')
def trial_completed(request):
    user = request.user
    trial_existing_objects = Trial.objects.filter(
        user=request.user
    )
    trial_existing = trial_existing_objects.last()
    number_of_trial = trial_existing.number_of_trial
    current_trial_completed = user.profile.trials_completed
    user.profile.trials_completed = current_trial_completed + 1
    user.save()

    return render(request, 'trial_completed.html',
                  {'trial_number': number_of_trial
                   })


def create_new_user(request):

    alphabet = ascii_letters + digits
    new_user_username = ''.join(
        secretschoice(alphabet) for i in range(8)
        )
    new_user_password = ''.join(
        secretschoice(alphabet) for i in range(14)
        )
    new_user = User.objects.create_user(
        new_user_username,
        'no_email@yahoo.co.uk',
        new_user_password
    )
    new_user.save()

    new_profile_list = Profile.objects.filter(user=new_user)
    new_profile = new_profile_list.last()

    # change the difficulty here
    #new_difficulty = randomchoice(four_by_four_setting_list)
    #new_difficulty = randomchoice(four_by_four_setting_list_two_options)
    new_difficulty = "very_easy"

    new_profile.low_medium_or_high_dots_setting = new_difficulty
    regret_forwards_boolean = randomchoice([True, False])
    new_profile.regret_forwards = regret_forwards_boolean
    new_profile.save()

    user_authenticated = authenticate(
        request,
        username=new_user_username,
        password=new_user_password
        )

    
    if user_authenticated is not None:
        login(request, user_authenticated)
        username_logged_in = user_authenticated.username
        return redirect('/user/' + username_logged_in)

    else:
        pass


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
        choice.first_or_second_choice = 1
        choice.save()

        result = Result()
        result.door_number = randint(1, 3)
        result.trial = trial_existing
        result.save()

        return redirect('/doorgame/door_result')
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

        return redirect('/doorgame/final_door_result')




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
                  'doorgame/door_page_one.html', {
                      "username": username_logged_in,
                  })


@login_required(login_url='accounts/login')
def door_result_page(request):
    if request.method == "POST":
        user_logged_in = request.user
        username_logged_in = user_logged_in.username
        choose_final_door(request)
        return redirect('/user/' + username_logged_in + '/final-door-result')
    # !----- Need to make choice specific to the user ----!

    # find the trials by this user
    trial_existing_objects = Trial.objects.filter(
        user=request.user
    )
    trial_existing = trial_existing_objects.last()
    choices_from_this_trial = Choice.objects.filter(
        trial=trial_existing
    )
    choice = choices_from_this_trial.last()
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
            # if there's a choice of 2 numbers to remove,
            # in this case they've already chosen the right number,
            # then remove at random one of the remaining 2 numbers.
            number_to_remove = randomchoice(possible_numbers)
        other_door_choice_list = [1, 2, 3]
        other_door_choice_list.remove(chosen_number)
        other_door_choice_list.remove(number_to_remove)
        number_to_change_to = other_door_choice_list[0]

        doors_to_display_list = [chosen_number,
                                 number_to_change_to
                                 ]
        if 1 in doors_to_display_list:
            door_one_bool = True
        else:
            door_one_bool = False
        if 2 in doors_to_display_list:
            door_two_bool = True
        else:
            door_two_bool = False
        if 3 in doors_to_display_list:
            door_three_bool = True
        else:
            door_three_bool = False

        return render(request, 'doorgame/door_result.html', {
            'door_chosen_number': str(choice.door_number),
            'door_to_remove_number': str(number_to_remove),
            'door_to_change_to_number': str(number_to_change_to),
            'door_one_bool': door_one_bool,
            'door_two_bool': door_two_bool,
            'door_three_bool': door_three_bool,
        })
    else:
        return render(request, 'doorgame/door_result.html',
                      )


def final_door_result_page(request):
    # find the trials by this user
    print('final_door_result_page called')
    trial_existing_objects = Trial.objects.filter(
        user=request.user
    )
    trial_existing = trial_existing_objects.last()
    trial_number = trial_existing.number_of_trial

    print(f'trial_number: {trial_number}')
    print(f'trial_limit: {settings.TRIAL_LIMIT}')

    if trial_number >= settings.TRIAL_LIMIT - 1:
        print('trial number condition satisfied, redirecting to regret url')
        return redirect('/doorgame/regret')
    else:
        print('trial_number is less than trial limit')
        return redirect('/memory_game/remember_memory_game')



@login_required(login_url='accounts/login')
def regret(request):
    user_logged_in = request.user
    regret_forwards_setting = user_logged_in.profile.regret_forwards

    return render(request, 'doorgame/regret.html', {
        'regret_forwards_setting': regret_forwards_setting
    })


@login_required(login_url='accounts/login')
def regret_completed(request):
    username_logged_in = request.user.username
    user = request.user

    survey_answers = SurveyAnswers()
    survey_answers.user = user

    # extract the regret value from the post submission
    regret_value = request.POST.get('regret_value')
    # assign to survey_answers the regret value
    survey_answers.regret_value = regret_value
    survey_answers.save()

    return redirect('/memory_game/remember_memory_game')

