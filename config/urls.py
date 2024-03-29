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
from doorgame import (
    views,
    views_prelim,
    views_post_game,
    views_memory_game,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    # Temporarily disabled new
    #path('new', views.site_maintenance, name='site_maintenance'),
    path('new', views.create_new_user, name='create_new_user'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views_prelim.home_page_user, name='home'),


    path('choose_door', views.choose_door, name='choose-door'),
    path('choose_final_door', views.choose_final_door, name='choose_final_door'),
    path('door_page_one', views.door_page_one, name="door-page-one"),

    # terms page - only first time they log in
    path('prelim/terms_and_conditions', views_prelim.terms_and_conditions, name='terms_and_conditions'),
    # consent questionnaire - only first time they log in
    path('prelim/consent_questions',views_prelim.consent_questions, name="consent_questions"),
    # Welcome page 1 - General explanation
    path('prelim/prelim_one', views_prelim.prelim_one, name="prelim_one"),
    # Welcome page 2 - Memory game explanation
    path('prelim/prelim_one_part_b', views_prelim.prelim_one_part_b, name='prelim_one_part_b'),
    # Memory game practise
    path('prelim_memory_game/prelim_two', views_prelim.prelim_two, name="prelim_two"),
    path('prelim_memory_game/prelim_three', views_prelim.prelim_three, name="prelim_three"),
    # Memory game feedback
    path('prelim_memory_game/prelim_three_part_b_feedback', views_prelim.prelim_three_part_b_feedback, name="prelim_three_part_b_feedback"),

    path('prelim_memory_game/prelim_two_second_go', views_prelim.prelim_two_second_go, name="prelim_two_second_go"),
    path('prelim_memory_game/prelim_three_second_go', views_prelim.prelim_three_second_go, name="prelim_three_second_go"),
    path('prelim_memory_game/prelim_three_part_b_feedback_second_go', views_prelim.prelim_three_part_b_feedback_second_go, name="prelim_three_part_b_feedback_second_go"),

    # Monty Hall introduction
    path('prelim/prelim_four', views_prelim.prelim_four, name="prelim_four"),
    path('prelim/prelim_five', views_prelim.prelim_five, name="prelim_five"),


    path('memory_game/memory_game_initial_turn', views_memory_game.memory_game_initial_turn, name="memory_game_initial_turn"),
    path('memory_game/memory_game_start/<trial_completed>', views_memory_game.memory_game_start, name="memory_game_start"),

    path('doorgame/door_result', views.door_result_page, name='door_result_page'),
    path('doorgame/regret', views.regret, name='regret'),
    path('doorgame/regret_completed', views.regret_completed, name='regret_completed'),
    path('doorgame/final_door_result', views.final_door_result_page, name='final_door_result_page'),

    path('memory_game/remember_memory_game', views_memory_game.remember_memory_game, name='remember_memory_game'),

    path('user', views_prelim.home_page_user, name='home-user'),
    path('user/<username>/', views_memory_game.home_page_memory_game, name='home_user_memory_game'),
    path('user/<username>/door_page_one', views.home_page_user_unique, name='home_user_unique'),

    path('memory_game/final_pattern', views_memory_game.final_pattern, name='final_pattern'),
    # Give decision of the outcome to the particpant -
    #### lost or won the Monty Hall game
    path('doorgame/outcome_of_doorgame', views.outcome_of_doorgame, name='outcome_of_doorgame'),

    path('trial_completed', views.trial_completed, name='trial_completed'),
    path('post_game/final_survey_one', views_post_game.final_survey_one, name='final_survey_one'),
    path('post_game/final_survey_one_completed', views_post_game.final_survey_one_completed, name='final_survey_one_completed'),
    path('post_game/final_survey_two_completed', views_post_game.final_survey_two_completed, name='final_survey_two_completed'),
    path('post_game/final_survey_three_completed', views_post_game.final_survey_three_completed, name='final_survey_three_completed'),
    path('post_game/final_completion', views_post_game.final_completion, name='final_completion'),

    #path('', TemplateView.as_view(template_name='home.html'), name='home'),
]
