from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings

from doorgame.models import (
    Trial,
    MemoryGame,
    MemoryGameHigh,
    MemoryGameList,
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

    # trials_completed = user_logged_in.profile.trials_completed

    # if trials_completed >= settings.TRIAL_LIMIT:
    #    return final_completion()

    number_of_trial = int(trial_completed) + 1
    if number_of_trial > settings.TRIAL_LIMIT:
        return final_completion()

    # number_of_trial = trials_completed + 1

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
