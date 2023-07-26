# changed name of random.choice so as not to confuse with
# the choice model instance
from random import choice as randomchoice

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import (
    authenticate,
    login
)
from django.contrib.auth.models import User
from django.conf import settings

from doorgame.models import (
    MemoryGamePrelim,
    MemoryGameHighPrelim,
    TrialPrelim,
    Profile
)
from .utils import (
    number_of_dots_selected_calculator_four_by_four,
    number_of_dots_correct_calculator_four_by_four,
    number_of_dots_selected_calculator,
    number_of_dots_correct_calculator,

)
from .dummy_memory_game import (
    MemoryGamePrelimClass,
    MemoryGamePrelimClassNineByNine
)


display_trial_limit = settings.TRIAL_LIMIT - 1
four_by_four_setting_list = ["very_hard", "medium", "very_easy"]
four_by_four_setting_list_two_options = ["medium", "very_easy"]

third_row_number_list = ['9', '10', '11', '12']
fourth_row_number_list = ['13', '14', '15', '16']
all_number_row_list = ['1', '2', '3', '4', '5', '6', '7',
                       '8', '9', '10', '11', '12', '13', '14', '15', '16']



@login_required(login_url='accounts/login')
def terms_and_conditions(request):
    return render(request, 'prelim/terms_and_conditions.html')


@login_required(login_url='accounts/login')
def home_page_user(request):
    username_logged_in = request.user.username
    if username_logged_in:
        return redirect('/prelim/terms_and_conditions')
    else:
        new_user_username = generate_username()[0]
        new_user_password = generate_username()[0]
        new_user = User.objects.create_user(
            new_user_username,
            'no_email@yahoo.co.uk',
            new_user_password
        )
        new_user.save()
        new_user_username = generate_username()[0]
        new_user_password = generate_username()[0]
        new_user = User.objects.create_user(
            new_user_username,
            'no_email@yahoo.co.uk',
            new_user_password
        )
        new_user.save()

        new_profile_list = Profile.objects.filter(user=new_user)
        new_profile = new_profile_list.last()

        new_difficulty = randomchoice(four_by_four_setting_list)
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

        new_profile_list = Profile.objects.filter(user=new_user)
        new_profile = new_profile_list.last()

        new_difficulty = randomchoice(four_by_four_setting_list)
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
def consent_questions(request):
    return render(request, 'prelim/consent_questions.html')


@login_required(login_url='accounts/login')
def prelim_one(request):
    return render(request, 'prelim/prelim_one.html')


@login_required(login_url='accounts/login')
def prelim_one_part_b(request):
    return render(request, 'prelim/prelim_one_part_b.html')


@login_required(login_url='accounts/login')
def prelim_two(request):
    user_logged_in = request.user
    very_hard_setting = user_logged_in.profile.low_medium_or_high_dots_setting
    easy_setting = user_logged_in.profile.hard_or_easy_dots

    if easy_setting:
        MemoryGamePrelim = MemoryGamePrelimClassNineByNine(1, easy_setting)

        return render(request, 'prelim_memory_game/prelim_two.html', {
            "memory_game": MemoryGamePrelim,
            "first_go": True
        })

    elif very_hard_setting:
        MemoryGamePrelim = MemoryGamePrelimClass(1, very_hard_setting)

        return render(request, 'prelim_memory_game/prelim_two_four_by_four.html', {
            "memory_game": MemoryGamePrelim,
            "first_go": True
        })

    else:
        print("Setting not assigned or other problem with setting!")
        return render(request, 'prelim_memory_game/prelim_two.html')


@login_required(login_url='accounts/login')
def prelim_two_second_go(request):
    user_logged_in = request.user
    very_hard_setting = user_logged_in.profile.low_medium_or_high_dots_setting
    if not very_hard_setting:
        class MemoryGamePrelimClassDummy:
            pass

        MemoryGamePrelim = MemoryGamePrelimClassDummy()

    if user_logged_in.profile.hard_or_easy_dots == 'easy':
        MemoryGamePrelim.box_1 = False
        MemoryGamePrelim.box_2 = False
        MemoryGamePrelim.box_3 = False
        MemoryGamePrelim.box_4 = True
        MemoryGamePrelim.box_5 = True
        MemoryGamePrelim.box_6 = True
        MemoryGamePrelim.box_7 = False
        MemoryGamePrelim.box_8 = False
        MemoryGamePrelim.box_9 = False
    elif user_logged_in.profile.hard_or_easy_dots == 'hard':
        MemoryGamePrelim.box_1 = True
        MemoryGamePrelim.box_2 = False
        MemoryGamePrelim.box_3 = True
        MemoryGamePrelim.box_4 = False
        MemoryGamePrelim.box_5 = True
        MemoryGamePrelim.box_6 = False
        MemoryGamePrelim.box_7 = False
        MemoryGamePrelim.box_8 = False
        MemoryGamePrelim.box_9 = True
    else:
        if very_hard_setting:
            MemoryGamePrelim = MemoryGamePrelimClass(2, very_hard_setting)
        return render(request, 'prelim_memory_game/prelim_two_four_by_four.html', {
            "memory_game": MemoryGamePrelim,
            "first_go": False
        })
    return render(request, 'prelim_memory_game/prelim_two.html', {
        "memory_game": MemoryGamePrelim,
        "first_go": False
    })


@login_required(login_url='accounts/login')
def prelim_three(request):
    # create two way choice, so that it will go to 3x3 or 4x4
    user_logged_in = request.user
    very_hard_setting = user_logged_in.profile.low_medium_or_high_dots_setting

    # if 4 by 4
    if very_hard_setting in four_by_four_setting_list:
        return render(request, 'prelim_memory_game/prelim_three_four_by_four.html',
                      {'repeat_example': True,
                       'third_row_number_list': third_row_number_list,
                       'fourth_row_number_list': fourth_row_number_list,
                       'all_number_row_list': all_number_row_list,
                       }
                      )
    # if 3 by 3:
    # print("This should be a 3 by 3 and will now return"
    #      "the prelim_three.html with the repeat_example variable set to True")
    return render(request, 'prelim_memory_game/prelim_three.html',
                  {'repeat_example': True
                   })


@login_required(login_url='accounts/login')
def prelim_three_part_b_feedback(request):
    user_logged_in = request.user
    very_hard_setting = user_logged_in.profile.low_medium_or_high_dots_setting
    easy_setting = user_logged_in.profile.hard_or_easy_dots

    # designate correct template
    if very_hard_setting in four_by_four_setting_list:
        feedback_template = 'prelim_memory_game/prelim_three_part_b_feedback_four_by_four.html'
    else:
        feedback_template = 'prelim_memory_game/prelim_three_part_b_feedback.html'

    if request.method == 'POST':
        if very_hard_setting in four_by_four_setting_list:
            memory_game = MemoryGameHighPrelim()
            memory_game_original = MemoryGamePrelimClass(1, very_hard_setting)
        else:
            print("very_hard_setting not given")
            memory_game = MemoryGamePrelim()
            memory_game_original = MemoryGamePrelimClassNineByNine(1, easy_setting)

        # if I can retrieve anything then the request should be true
        # if not then it should be false
        user_logged_in = request.user
        username_logged_in = user_logged_in.username

        # find the trials by this user

        trial_existing = TrialPrelim()
        trial_existing.save()
        memory_game.trial = trial_existing
        # if I can retrieve anything then the request should be true
        # if not then it should be false

        if request.POST.get('box_1') == "True":
            memory_game.box_1 = True
        if request.POST.get('box_2') == "True":
            memory_game.box_2 = True
        if request.POST.get('box_3') == "True":
            memory_game.box_3 = True
        if request.POST.get('box_4') == "True":
            memory_game.box_4 = True
        if request.POST.get('box_5') == "True":
            memory_game.box_5 = True
        if request.POST.get('box_6') == "True":
            memory_game.box_6 = True
        if request.POST.get('box_7') == "True":
            memory_game.box_7 = True
        if request.POST.get('box_8') == "True":
            memory_game.box_8 = True
        if request.POST.get('box_9') == "True":
            memory_game.box_9 = True

        if very_hard_setting in four_by_four_setting_list:
            if request.POST.get('box_10') == "True":
                memory_game.box_10 = True
            if request.POST.get('box_11') == "True":
                memory_game.box_11 = True
            if request.POST.get('box_12') == "True":
                memory_game.box_12 = True
            if request.POST.get('box_13') == "True":
                memory_game.box_13 = True
            if request.POST.get('box_14') == "True":
                memory_game.box_14 = True
            if request.POST.get('box_15') == "True":
                memory_game.box_15 = True
            if request.POST.get('box_16') == "True":
                memory_game.box_16 = True

        memory_game.initial_or_final = 'initial'
        memory_game.save()

        if very_hard_setting in four_by_four_setting_list:
            number_of_dots_in_original_memory_game = number_of_dots_selected_calculator_four_by_four(
                memory_game_original)
            number_of_dots_correct = number_of_dots_correct_calculator_four_by_four(
                memory_game_original, memory_game)
        else:
            number_of_dots_in_original_memory_game = number_of_dots_selected_calculator(
                memory_game_original)
            number_of_dots_correct = number_of_dots_correct_calculator(
                memory_game_original, memory_game)
        # To address bug where they score more than possible:
        if number_of_dots_correct > number_of_dots_in_original_memory_game:
            number_of_dots_correct = number_of_dots_in_original_memory_game

        if very_hard_setting in four_by_four_setting_list:
            number_of_dots_selected = number_of_dots_selected_calculator_four_by_four(
                memory_game)
        else:
            number_of_dots_selected = number_of_dots_selected_calculator(
                memory_game
            )
        if number_of_dots_selected <= number_of_dots_in_original_memory_game:
            excess_dots_message = False
        elif number_of_dots_selected > number_of_dots_in_original_memory_game:
            excess_dots_message = True
        else:
            print(
                "Error: Number of dots have not been compared correctly, is the data in the right format")

        return render(request, feedback_template,
                      {'repeat_example': True,
                       'memory_game': memory_game,
                       'memory_game_original': memory_game_original,
                       'number_of_dots_total': number_of_dots_in_original_memory_game,
                       'number_of_dots_correct': number_of_dots_correct,
                       'excess_dots_message': excess_dots_message,
                       })

    # If not a POST request then just return html
    return render(request, feedback_template)


@login_required(login_url='accounts/login')
def prelim_three_second_go(request):
    user_logged_in = request.user
    very_hard_setting = user_logged_in.profile.low_medium_or_high_dots_setting
    if very_hard_setting in four_by_four_setting_list:
        return render(request, 'prelim_memory_game/prelim_three_four_by_four.html',
                      {'repeat_example': False,
                       'third_row_number_list': third_row_number_list,
                       'fourth_row_number_list': fourth_row_number_list,
                       'all_number_row_list': all_number_row_list,
                       }
                      )
    return render(request, 'prelim_memory_game/prelim_three.html',
                  {'repeat_example': False
                   })


@login_required(login_url='accounts/login')
def prelim_three_part_b_feedback_second_go(request):
    user_logged_in = request.user
    very_hard_setting = user_logged_in.profile.low_medium_or_high_dots_setting
    easy_setting = user_logged_in.profile.hard_or_easy_dots

    # designate correct template
    if very_hard_setting in four_by_four_setting_list:
        feedback_template = 'prelim_memory_game/prelim_three_part_b_feedback_four_by_four.html'
    else:
        feedback_template = 'prelim_memory_game/prelim_three_part_b_feedback.html'

    if request.method == 'POST':
        if very_hard_setting in four_by_four_setting_list:
            memory_game = MemoryGameHighPrelim()
            memory_game_original = MemoryGamePrelimClass(2, very_hard_setting)
        else:
            print("very_hard_setting not given")
            memory_game = MemoryGamePrelim()
            memory_game_original = MemoryGamePrelimClassNineByNine(2, easy_setting)

        # if I can retrieve anything then the request should be true
        # if not then it should be false
        user_logged_in = request.user
        username_logged_in = user_logged_in.username

        # find the trials by this user

        trial_existing = TrialPrelim()
        trial_existing.save()
        memory_game.trial = trial_existing
        # if I can retrieve anything then the request should be true
        # if not then it should be false

        if request.POST.get('box_1') == "True":
            memory_game.box_1 = True
        if request.POST.get('box_2') == "True":
            memory_game.box_2 = True
        if request.POST.get('box_3') == "True":
            memory_game.box_3 = True
        if request.POST.get('box_4') == "True":
            memory_game.box_4 = True
        if request.POST.get('box_5') == "True":
            memory_game.box_5 = True
        if request.POST.get('box_6') == "True":
            memory_game.box_6 = True
        if request.POST.get('box_7') == "True":
            memory_game.box_7 = True
        if request.POST.get('box_8') == "True":
            memory_game.box_8 = True
        if request.POST.get('box_9') == "True":
            memory_game.box_9 = True

        if very_hard_setting in four_by_four_setting_list:
            if request.POST.get('box_10') == "True":
                memory_game.box_10 = True
            if request.POST.get('box_11') == "True":
                memory_game.box_11 = True
            if request.POST.get('box_12') == "True":
                memory_game.box_12 = True
            if request.POST.get('box_13') == "True":
                memory_game.box_13 = True
            if request.POST.get('box_14') == "True":
                memory_game.box_14 = True
            if request.POST.get('box_15') == "True":
                memory_game.box_15 = True
            if request.POST.get('box_16') == "True":
                memory_game.box_16 = True

        memory_game.initial_or_final = 'initial'
        memory_game.save()

        if very_hard_setting in four_by_four_setting_list:
            number_of_dots_in_original_memory_game = number_of_dots_selected_calculator_four_by_four(
                memory_game_original)
            number_of_dots_correct = number_of_dots_correct_calculator_four_by_four(
                memory_game_original, memory_game)
        else:
            number_of_dots_in_original_memory_game = number_of_dots_selected_calculator(
                memory_game_original)
            number_of_dots_correct = number_of_dots_correct_calculator(
                memory_game_original, memory_game)

        # To address bug where they score more than possible:
        if number_of_dots_correct > number_of_dots_in_original_memory_game:
            number_of_dots_correct = number_of_dots_in_original_memory_game

        if very_hard_setting in four_by_four_setting_list:
            number_of_dots_selected = number_of_dots_selected_calculator_four_by_four(
                memory_game
            )
        else:
            number_of_dots_selected = number_of_dots_selected_calculator(
                memory_game
            )
        if number_of_dots_selected <= number_of_dots_in_original_memory_game:
            excess_dots_message = False
        elif number_of_dots_selected > number_of_dots_in_original_memory_game:
            excess_dots_message = True
        else:
            print(
                "Error: Number of dots have not been compared correctly, is the data in the right format")

    return render(request, feedback_template,
                  {'repeat_example': False,
                   'memory_game': memory_game,
                   'memory_game_original': memory_game_original,
                   'number_of_dots_total': number_of_dots_in_original_memory_game,
                   'number_of_dots_correct': number_of_dots_correct,
                   'excess_dots_message': excess_dots_message,
                   })


def prelim_four(request):
    return render(request, 'prelim/prelim_four.html',
                  {'display_trial_limit': display_trial_limit
                   })


def prelim_five(request):
    return render(request, 'prelim/prelim_five.html')


