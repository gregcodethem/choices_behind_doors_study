from django.contrib import admin

from .models import Trial, Choice, MemoryGame, SurveyAnswers


admin.site.register(Trial)
admin.site.register(Choice)
admin.site.register(MemoryGame)
admin.site.register(SurveyAnswers)