from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.
def home_page(request):
	if request.method == 'POST':
		return redirect('/door-result')
	return render(request, 'home.html')

def door_result_page(request):
	return render(request, 'door_result.html', {
		'door_chosen_text': request.POST.get('door_chosen', '')
		})