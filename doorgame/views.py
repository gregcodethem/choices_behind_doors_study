from django.shortcuts import render, redirect
from django.http import HttpResponse
from doorgame.models import Choice
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

# Create your views here.


def home_page(request, user=None):
    if request.method == 'POST':
        choice = Choice()
        choice.door_number = request.POST.get('door_chosen', 0)
        choice.save()

        return redirect('/door-result')
    return render(request, 'home.html')

@login_required(login_url='accounts/login')
def home_page_user(request):
    username_logged_in = request.user.username
    if username_logged_in:
        return redirect('/user/'+username_logged_in)

    else:
        return render(request, 'home.html')

@login_required(login_url='accounts/login')
def home_page_user_unique(request, username):
    username_logged_in = request.user.username
    return render(request, 'home.html', {"username": username_logged_in})

def door_result_page(request):
    choice = Choice.objects.last()
    if choice:
        return render(request, 'door_result.html', {
            'door_chosen_text': 'door' + str(choice.door_number)
        })
    else:
        return render(request, 'door_result.html',
                      )
