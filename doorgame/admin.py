from django.contrib import admin

from .models import Trial, Choice, MemoryGame, SurveyAnswers, MemoryGameList, Profile, Result


admin.site.register(Trial)
admin.site.register(Choice)
admin.site.register(MemoryGame)
admin.site.register(MemoryGameList)
admin.site.register(SurveyAnswers)
admin.site.register(Profile)
admin.site.register(Result)