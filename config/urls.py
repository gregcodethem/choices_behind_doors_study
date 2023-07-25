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
    # Temporarily disabled new
    #path('new', views.site_maintenance, name='site_maintenance'),
    path('new', views.create_new_user, name='create_new_user'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.home_page_user, name='home'),
    #path('door-result', views.door_result_page, name='door_result_page'),


    # Other memory game

    # Regret page - rank 1 - 7

    # Then remember the dots page

    # Give decision of the outcome to the particpant -
    #### lost or won the Monty Hall game

    # Final questionnaire - streamed down version of existing questionnaire pages.

    path('choose_door', views.choose_door, name='choose-door'),
    path('choose_final_door', views.choose_final_door, name='choose_final_door'),
    path('door_page_one', views.door_page_one, name="door-page-one"),

    # terms page - only first time they log in
    path('prelim/terms_and_conditions', views.terms_and_conditions, name='terms_and_conditions'),
    # consent questionnaire - only first time they log in
    path('prelim/consent_questions',views.consent_questions, name="consent_questions"),
    # Welcome page 1 - General explanation
    path('prelim/prelim_one', views.prelim_one, name="prelim_one"),
    # Welcome page 2 - Memory game explanation
    path('prelim/prelim_one_part_b',
        views.prelim_one_part_b,
        name='prelim_one_part_b'),
    # Memory game practise
    path('prelim_memory_game/prelim_two', views.prelim_two, name="prelim_two"),
    path('prelim_memory_game/prelim_three', views.prelim_three, name="prelim_three"),
    # Memory game feedback
    path('prelim_memory_game/prelim_three_part_b_feedback', views.prelim_three_part_b_feedback, name="prelim_three_part_b_feedback"),

    path('prelim_memory_game/prelim_two_second_go', views.prelim_two_second_go, name="prelim_two_second_go"),
    path('prelim_memory_game/prelim_three_second_go', views.prelim_three_second_go, name="prelim_three_second_go"),
    path('prelim_memory_game/prelim_three_part_b_feedback_second_go', views.prelim_three_part_b_feedback_second_go, name="prelim_three_part_b_feedback_second_go"),

    # Monty Hall introduction
    path('prelim/prelim_four', views.prelim_four, name="prelim_four"),
    path('prelim/prelim_five', views.prelim_five, name="prelim_five"),


    path('memory_game/memory_game_initial_turn', views.memory_game_initial_turn, name="memory_game_initial_turn"),
    path('memory_game/memory_game_start/<trial_completed>', views.memory_game_start, name="memory_game_start"),


    path('user/<username>/door-result', views.door_result_page, name='door_result_page_old'),
    path('doorgame/door_result', views.door_result_page, name='door_result_page'),
    path('user/<username>/final-door-result', views.final_door_result_page, name='final_door_result_page'),
    path('regret', views.regret, name='regret'),
    path('regret_completed', views.regret_completed, name='regret_completed'),


    path('memory_game/remember_memory_game', views.remember_memory_game, name='remember_memory_game'),


    path('user', views.home_page_user, name='home-user'),
    path('user/<username>/',
         views.home_page_memory_game,
         name='home_user_memory_game'
         ),
    path('user/<username>/door_page_one',
         views.home_page_user_unique,
         name='home_user_unique'
         ),

    path('final_pattern', views.final_pattern, name='final_pattern'),
    path('outcome_of_doorgame', views.outcome_of_doorgame, name='outcome_of_doorgame'),
    path('trial_completed', views.trial_completed, name='trial_completed'),
    path('final_survey_one', views.final_survey_one, name='final_survey_one'),
    path('final_survey_one_completed', views.final_survey_one_completed, name='final_survey_one_completed'),
    path('final_survey_two_completed', views.final_survey_two_completed, name='final_survey_two_completed'),
    path('final_survey_three_completed', views.final_survey_three_completed, name='final_survey_three_completed'),
    path('final_completion', views.final_completion, name='final_completion'),


    #path('', TemplateView.as_view(template_name='home.html'), name='home'),
]
