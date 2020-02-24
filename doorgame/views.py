from django.shortcuts import render

# Create your views here.
def home_page(request):
	return render(request, 'home.html')

def door_result_page(request):
	return render(request, 'door_result.html')