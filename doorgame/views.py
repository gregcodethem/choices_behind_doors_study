from django.shortcuts import render, redirect
from django.http import HttpResponse
from doorgame.models import Choice

# Create your views here.


def home_page(request):
    if request.method == 'POST':
        choice = Choice()
        choice.door_number = request.POST.get('door_chosen', 0)
        choice.save()

        return redirect('/door-result')
    return render(request, 'home.html')

def door_one_page(request):
    if request.method == 'POST':
        choice = Choice()
        choice.door_number = 1
        choice.save()

    return redirect('/door-result')

def door_two_page(request):
    if request.method == 'POST':
        choice = Choice()
        choice.door_number = 2
        choice.save()

    return redirect('/door-result')

def door_three_page(request):
    if request.method == 'POST':
        choice = Choice()
        choice.door_number = 3
        choice.save()

    return redirect('/door-result')

def door_result_page(request):
    choice = Choice.objects.last()
    if choice:
        return render(request, 'door_result.html', {
            'door_chosen_text': 'door' + str(choice.door_number)
        })
    else:
        return render(request, 'door_result.html',
                      )
