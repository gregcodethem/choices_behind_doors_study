from random import randint
# changed name of random.choice so as not to confuse with
# the choice model instance
from random import choice as randomchoice

from django.shortcuts import render, redirect
from django.http import HttpResponse
from doorgame.models import Choice, Trial, Result, MemoryGame
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

# Create your views here.


def home_page(request, user=None):
    return redirect('/user')

@login_required(login_url='accounts/login')
def final_pattern(request, username):
    username_logged_in = request.user.username
    if request.method == 'POST':
        memory_game = MemoryGame()
        memory_game.box_1 = request.POST.get('box_1')
        memory_game.box_2 = request.POST.get('box_2')
        memory_game.initial_or_final = 'final'
        memory_game.save()
        return redirect('/user' + username_logged_in)

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
        trial = Trial()
        trial.user = request.user
        trial.save()
        choice = Choice()
        choice.door_number = request.POST.get('door_chosen', 0)
        choice.trial = trial
        choice.save()

        result = Result()
        result.door_number = randint(1, 3)
        result.trial = trial
        result.save()

        return redirect('/user/' + username_logged_in + '/door-result')
    else:
        pass


@login_required(login_url='accounts/login')
def choose_final_door(request):
    if request.method == 'POST':
        user_logged_in = request.user
        username_logged_in = user_logged_in.username
        
        #find the trials by this user
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
        #insert method to remember pattern here (if necessary)
        return redirect('/user/' + username_logged_in + '/door-page-one')

    else:
        pass # insert some method here to generate the pattern

    return render(request, 'home.html', {"username": username_logged_in})   

@login_required(login_url='accounts/login')
def door_page_one(request):
    username_logged_in = request.user.username
    if request.method == "POST":
        return redirect('/user/' + username_logged_in + '/door_page_one')

@login_required(login_url='accounts/login')
def home_page_user_unique(request, username):
    username_logged_in = request.user.username
    user_logged_in = request.user

    if request.method == 'POST':
        choose_door(request)
        return redirect('/user/' + username_logged_in + '/door-result')

    return render(request, 'door-page-one.html', {"username": username_logged_in})


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
