from django.shortcuts import render, redirect
from django.http import HttpResponse
from doorgame.models import Choice, Trial
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

# Create your views here.


def home_page(request, user=None):
    return redirect('/user')


@login_required(login_url='accounts/login')
def home_page_user(request):
    username_logged_in = request.user.username
    if username_logged_in:
        return redirect('/user/'+username_logged_in)

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
        return redirect('/user/' + username_logged_in + '/door-result')
    else:
        pass


@login_required(login_url='accounts/login')
def home_page_user_unique(request, username):
    username_logged_in = request.user.username
    user_logged_in = request.user
    
    if request.method == 'POST':
        choose_door(request)
        return redirect('/user/' + username_logged_in + '/door-result')4

    
    return render(request, 'home.html', {"username": username_logged_in})


def door_result_page(request, username):
    choice = Choice.objects.last()
    if choice:
        return render(request, 'door_result.html', {
            'door_chosen_text': 'door' + str(choice.door_number)
        })
    else:
        return render(request, 'door_result.html',
                      )
