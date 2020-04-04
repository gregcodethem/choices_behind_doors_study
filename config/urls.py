"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from doorgame import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.home_page_user, name='home'),
    #path('door-result', views.door_result_page, name='door_result_page'),
    path('choose_door', views.choose_door, name='choose-door'),
    path('choose_final_door', views.choose_final_door, name='choose_final_door'),
    path('door_page_one', views.door_page_one, name="door-page-one"),
    path('prelim_two', views.prelim_two, name="prelim_two"),
    path('prelim_three', views.prelim_three, name="prelim_three"),
    path('prelim_four', views.prelim_four, name="prelim_four"),
    path('user/<username>/door-result',
         views.door_result_page,
         name='door_result_page'
         ),
    path('user/<username>/final-door-result',
         views.final_door_result_page,
         name='final_door_result_page'
         ),
    path('user', views.home_page_user, name='home-user'),
    path('user/<username>/',
         views.home_page_memory_game,
         name='home_user_memory_game'
         ),
    path('user/<username>/door_page_one',
         views.home_page_user_unique,
         name='home_user_unique'
         ),
    path('final_pattern',
        views.final_pattern,
        name='final_pattern'
        ),
    path('user/<username>/final_survey_one',
        views.final_survey_one,
        name='final_survey_one'),
    path('final_survey_one_completed',
        views.final_survey_one_completed,
        name='final_survey_one_completed'),
    path('final_survey_two_completed',
        views.final_survey_two_completed,
        name='final_survey_two_completed'),
    path('final_survey_three_completed',
        views.final_survey_three_completed,
        name='final_survey_three_completed'),
    #path('', TemplateView.as_view(template_name='home.html'), name='home'),
]
