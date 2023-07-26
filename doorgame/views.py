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
    MemoryGame,
    MemoryGameHigh,
    SurveyAnswers,
    MemoryGameList,
    Profile
)
from .utils import (
    add_memory_games,
    add_four_by_four_memory_games,
)

display_trial_limit = settings.TRIAL_LIMIT - 1
four_by_four_setting_list = ["very_hard", "medium", "very_easy"]
four_by_four_setting_list_two_options = ["medium", "very_easy"]

third_row_number_list = ['9', '10', '11', '12']
fourth_row_number_list = ['13', '14', '15', '16']
all_number_row_list = ['1', '2', '3', '4', '5', '6', '7',
                       '8', '9', '10', '11', '12', '13', '14', '15', '16']

def site_maintenance(request):
    return HttpResponse('<html><title>Site under maintenance</title><h1>Site under maintenance, we will be back online soon</h1></html>')


def home_page(request, user=None):
    return redirect('/user')


@login_required(login_url='accounts/login')
def remember_memory_game(request):
    user_logged_in = request.user
    very_hard_setting = user_logged_in.profile.low_medium_or_high_dots_setting

    if very_hard_setting in four_by_four_setting_list:
        remember_memory_game_page_string = 'remember_memory_game_four_by_four.html'
        all_number_row_list = ['1', '2', '3', '4', '5', '6', '7',
                               '8', '9', '10', '11', '12', '13', '14', '15', '16']
        return render(request, remember_memory_game_page_string, {
            'third_row_number_list': third_row_number_list,
            'fourth_row_number_list': fourth_row_number_list,
            'all_number_row_list': all_number_row_list,
        })
    else:
        remember_memory_game_page_string = 'memory_game/remember_memory_game.html'
        return render(request, remember_memory_game_page_string)


@login_required(login_url='accounts/login')
def final_pattern(request):
    username_logged_in = request.user.username
    user_logged_in = request.user
    very_hard_setting = user_logged_in.profile.low_medium_or_high_dots_setting
    hard_or_easy_dots_setting = user_logged_in.profile.hard_or_easy_dots

    if request.method == 'POST':
        if very_hard_setting in four_by_four_setting_list:
            memory_game = MemoryGameHigh()
        else:
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

        # Get total of trues, if greater than what it should be according
        # to  the difficulty level then send it back to the previous page
        # without saving and with an error message
        if very_hard_setting == "very_hard":
            number_of_dots_to_select = 6
        elif hard_or_easy_dots_setting == 'easy':
            number_of_dots_to_select = 3
        else:
            number_of_dots_to_select = 4

        dots_selected_in_final_patttern = 0

        if request.POST.get('box_1') == "True":
            memory_game.box_1 = True
            dots_selected_in_final_patttern += 1
        if request.POST.get('box_2') == "True":
            memory_game.box_2 = True
            dots_selected_in_final_patttern += 1
        if request.POST.get('box_3') == "True":
            memory_game.box_3 = True
            dots_selected_in_final_patttern += 1
        if request.POST.get('box_4') == "True":
            memory_game.box_4 = True
            dots_selected_in_final_patttern += 1
        if request.POST.get('box_5') == "True":
            memory_game.box_5 = True
            dots_selected_in_final_patttern += 1
        if request.POST.get('box_6') == "True":
            memory_game.box_6 = True
            dots_selected_in_final_patttern += 1
        if request.POST.get('box_7') == "True":
            memory_game.box_7 = True
            dots_selected_in_final_patttern += 1
        if request.POST.get('box_8') == "True":
            memory_game.box_8 = True
            dots_selected_in_final_patttern += 1
        if request.POST.get('box_9') == "True":
            memory_game.box_9 = True
            dots_selected_in_final_patttern += 1

        if very_hard_setting in four_by_four_setting_list:
            if request.POST.get('box_10') == "True":
                memory_game.box_10 = True
                dots_selected_in_final_patttern += 1
            if request.POST.get('box_11') == "True":
                memory_game.box_11 = True
                dots_selected_in_final_patttern += 1
            if request.POST.get('box_12') == "True":
                memory_game.box_12 = True
                dots_selected_in_final_patttern += 1
            if request.POST.get('box_13') == "True":
                memory_game.box_13 = True
                dots_selected_in_final_patttern += 1
            if request.POST.get('box_14') == "True":
                memory_game.box_14 = True
                dots_selected_in_final_patttern += 1
            if request.POST.get('box_15') == "True":
                memory_game.box_15 = True
                dots_selected_in_final_patttern += 1
            if request.POST.get('box_16') == "True":
                memory_game.box_16 = True
                dots_selected_in_final_patttern += 1

        if dots_selected_in_final_patttern != number_of_dots_to_select:
            remember_memory_game_page_string = 'memory_game/remember_memory_game_four_by_four.html'
            
            if dots_selected_in_final_patttern < number_of_dots_to_select:
                error_message_number_of_dots = f"There are not enough dots, there should be {str(number_of_dots_to_select)}"
            elif dots_selected_in_final_patttern > number_of_dots_to_select:
                error_message_number_of_dots = f"There are too many dots, there should be {str(number_of_dots_to_select)}"
            return render(request, remember_memory_game_page_string, {
                'third_row_number_list': third_row_number_list,
                'fourth_row_number_list': fourth_row_number_list,
                'all_number_row_list': all_number_row_list,
                'error_message_number_of_dots': error_message_number_of_dots
            })


        memory_game.initial_or_final = 'final'
        memory_game.save()

        trial_number = trial_existing.number_of_trial
        if trial_number >= settings.TRIAL_LIMIT - 1:
            return redirect('/doorgame/outcome_of_doorgame')
        return redirect('/trial_completed')

    else:
        print("final_pattern_step has NOT registered post request")
    return redirect('/user/' + username_logged_in)


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
def memory_game_initial_turn(request):
    user_logged_in = request.user
    username_logged_in = request.user.username

    memory_game_list_prelim = MemoryGameList.objects.filter(
        user=user_logged_in)
    print(f'first instance of memory game list {memory_game_list_prelim}')

    # check so it doesn't run this script again
    if len(memory_game_list_prelim) == 0:
        print('len of memory game list was 0, so creating new memory_game_list model')
        memory_game_list = MemoryGameList()
        memory_game_list.user = user_logged_in
        memory_game_list.save()

        # find whether user is registered as easy or hard dot list
        if user_logged_in.profile:
            hard_or_easy_dot_list = user_logged_in.profile.hard_or_easy_dots
            very_hard_dot_list_setting = user_logged_in.profile.low_medium_or_high_dots_setting
            print(f'setting:{very_hard_dot_list_setting}')

            if very_hard_dot_list_setting == "very_hard":
                print('very_hard_setting_activated in memory_game_initial_turn')
                add_four_by_four_memory_games(
                    memory_game_list, dot_list == "very_hard")
            elif very_hard_dot_list_setting == "medium":
                print('4 by 4 medium setting activated in memory_game_initial_turn')
                add_four_by_four_memory_games(
                    memory_game_list, dot_list == "medium")
            elif very_hard_dot_list_setting == "very_easy":
                print('4 by 4 very_easy setting activated in memory_game_initial_turn')
                add_four_by_four_memory_games(
                    memory_game_list, dot_list == "very_easy")
            elif hard_or_easy_dot_list == "easy":
                add_memory_games(memory_game_list, "easy")
            elif hard_or_easy_dot_list == "hard":
                print("hard setting activated")
                add_memory_games(memory_game_list, "hard")
            else:
                print(
                    "Error: hard_or_easy_dots setting in incorrect format in Profile model")
                print("Adding hard list")
                add_memory_games(memory_game_list, dot_list="hard")
        else:
            print("profile not logged in, so hard setting activated as backup")
            add_memory_games(memory_game_list, dot_list="hard")
        memory_game_list = [memory_game_list]
    else:
        memory_game_list = memory_game_list_prelim

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

    very_hard_setting = user_logged_in.profile.low_medium_or_high_dots_setting

    if very_hard_setting in four_by_four_setting_list:
        home_page_string = 'memory_game/home_four_by_four.html'
        MemoryGameToSave = MemoryGameHigh
    else:
        home_page_string = 'memory_game/home.html'
        MemoryGameToSave = MemoryGame

    if len(memory_game_list) != 0:
        memory_game_list_end = MemoryGameToSave.objects.filter(
            memory_game_list=memory_game_list[0],
            number_of_trial=number_of_trial
        )
        memory_game = memory_game_list_end[0]
        memory_game.trial = trial
        memory_game.save()


    return render(request, home_page_string, {
        "username": username_logged_in,
        "number_of_trial": number_of_trial,
        "memory_game": memory_game,
    })


@login_required(login_url='accounts/login')
def memory_game_start(request, trial_completed):
    user_logged_in = request.user
    username_logged_in = request.user.username

    #trials_completed = user_logged_in.profile.trials_completed

    # if trials_completed >= settings.TRIAL_LIMIT:
    #    return final_completion()

    number_of_trial = int(trial_completed) + 1
    if number_of_trial > settings.TRIAL_LIMIT:
        return final_completion()

    #number_of_trial = trials_completed + 1

    new_trial = Trial()
    new_trial.user = user_logged_in
    new_trial.number_of_trial = number_of_trial
    new_trial.save()

    very_hard_setting = user_logged_in.profile.low_medium_or_high_dots_setting

    if very_hard_setting in four_by_four_setting_list:
        MemoryGameToGet = MemoryGameHigh
    else:
        MemoryGameToGet = MemoryGame

    memory_game_list_from_setup = MemoryGameList.objects.get(
        user=user_logged_in)

    memory_game = MemoryGameToGet.objects.get(
        memory_game_list=memory_game_list_from_setup,
        number_of_trial=number_of_trial
    )
    memory_game.trial = new_trial
    memory_game.save()

    if very_hard_setting in four_by_four_setting_list:
        home_page_string = 'memory_game/home_four_by_four.html'

    else:
        home_page_string = 'memory_game/home.html'

    return render(request, home_page_string, {
        "username": username_logged_in,
        "number_of_trial": number_of_trial,
        "memory_game": memory_game,
    })


@login_required(login_url='accounts/login')
def home_page_memory_game(request, username):

    # logout_if_reached_the_limit(request)
    user_logged_in = request.user
    if user_logged_in.profile.trials_completed >= settings.TRIAL_LIMIT:
        return final_completion(request)

    trials_for_this_user = Trial.objects.filter(user=user_logged_in)
    if len(trials_for_this_user) != 0:
        latest_trial = trials_for_this_user.last()

        if latest_trial.number_of_trial >= settings.TRIAL_LIMIT:
            return final_completion(request)

        else:
            pass

    username_logged_in = request.user.username
    user_logged_in = request.user

    if request.method == 'POST':
        # insert method to remember pattern here (if necessary)
        return redirect('/user/' + username_logged_in + '/door-page-one')

    else:

        memory_game_list_prelim = MemoryGameList.objects.filter(
            user=user_logged_in)
        print(f'first instance of memory game list {memory_game_list_prelim}')
        if len(memory_game_list_prelim) == 0:
            print('len of memory game list was 0, so creating new memory_game_list model')
            memory_game_list = MemoryGameList()
            memory_game_list.user = user_logged_in
            memory_game_list.save()

            # find whether user is registered as easy or hard dot list
            if user_logged_in.profile:
                hard_or_easy_dot_list = user_logged_in.profile.hard_or_easy_dots
                very_hard_dot_list_setting = user_logged_in.profile.low_medium_or_high_dots_setting

                print(f'setting:{very_hard_dot_list_setting}')

                if very_hard_dot_list_setting == "very_hard":
                    print('very_hard_setting_activated in home_page_memory_game')
                    add_four_by_four_memory_games(
                        memory_game_list, dot_list="very_hard")
                elif very_hard_dot_list_setting == "medium":
                    print('4 by 4 medium setting activated in home_page_memory_game')
                    add_four_by_four_memory_games(
                        memory_game_list, dot_list="medium")
                elif very_hard_dot_list_setting == "very_easy":
                    print('4 by 4 very_easy setting activated in home_page_memory_game')
                    add_four_by_four_memory_games(
                        memory_game_list, dot_list="very_easy")

                elif hard_or_easy_dot_list == "easy":
                    add_memory_games(memory_game_list, "easy")
                elif hard_or_easy_dot_list == "hard":
                    add_memory_games(memory_game_list, "hard")
                else:
                    print(
                        "Error: hard_or_easy_dots setting in incorrect format in Profile model")
                    print("Adding hard list")
                    add_memory_games(memory_game_list, dot_list="hard")
            else:
                add_memory_games(memory_game_list, dot_list="hard")
            memory_game_list = [memory_game_list]
        else:
            memory_game_list = memory_game_list_prelim

        trial = Trial()
        trial.user = request.user

        trials_for_this_user = Trial.objects.filter(user=user_logged_in)
        latest_trial = trials_for_this_user.last()
        if len(trials_for_this_user) != 0:
            number_of_trial = latest_trial.number_of_trial + 1
        else:
            number_of_trial = 0
        trial.number_of_trial = number_of_trial
        trial.save()

        # !!!!!----- This is the bit I need to change so
        # that it's seeing the different patterns
        # insert some method here to generate the pattern

        if len(memory_game_list) != 0:

            very_hard_setting = user_logged_in.profile.low_medium_or_high_dots_setting

            if very_hard_setting in four_by_four_setting_list:
                MemoryGameToSave = MemoryGameHigh
            else:
                MemoryGameToSave = MemoryGame

            memory_game_list_end = MemoryGameToSave.objects.filter(
                memory_game_list=memory_game_list[0],
                number_of_trial=number_of_trial
            )
            if len(memory_game_list_end) != 0:
                memory_game = memory_game_list_end[0]
            else:
                # This is a bit of a hack to stop it crashing when
                # people log in after completing everything.
                return final_completion(request)
            memory_game.trial = trial
            memory_game.save()

    # find if prelim has been completed
    prelim_completed_bool = user_logged_in.profile.prelim_completed 


    if number_of_trial == 0 or prelim_completed_bool == False:
        return render(request, 'prelim/terms_and_conditions.html', {
            "username": username_logged_in,
            "number_of_trial": number_of_trial,
            "memory_game": memory_game,
        }
                      )

    return render(request, 'memory_game/home.html', {
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

