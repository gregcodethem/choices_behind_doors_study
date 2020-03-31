from django.db import models
from django.contrib.auth.models import User

class SurveyAnswers(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        default=None,
        null=True
    )
    best_strategy = models.TextField(default="blank")
    estimate_stayed_lost = models.IntegerField(default=0)
    estimate_stayed_won = models.IntegerField(default=0)
    estimate_switched_lost = models.IntegerField(default=0)
    estimate_switched_won = models.IntegerField(default=0)
    age = models.IntegerField(default=0)
    familiar = models.TextField(default="blank")
    gender = models.TextField(default="blank")
    education_level = models.TextField(default="blank")

class Trial(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        default=None,
        null=True
    )
    number_of_trial = models.IntegerField(default=0)


class MemoryGame(models.Model):
    trial = models.ForeignKey(
        Trial,
        on_delete=models.CASCADE,
        default=None,
        null=True
    )
    box_1 = models.BooleanField(default=False)
    box_2 = models.BooleanField(default=False)
    box_3 = models.BooleanField(default=False)
    box_4 = models.BooleanField(default=False)
    box_5 = models.BooleanField(default=False)
    box_6 = models.BooleanField(default=False)
    box_7 = models.BooleanField(default=False)
    box_8 = models.BooleanField(default=False)
    box_9 = models.BooleanField(default=False)

    initial_or_final = models.CharField(max_length=15, default="")



class Choice(models.Model):
    door_number = models.IntegerField(default=0)
    first_or_second_choice = models.IntegerField(default=0)
    trial = models.ForeignKey(
        Trial,
        on_delete=models.CASCADE,
        default=None,
        null=True
    )


class Result(models.Model):
    door_number = models.IntegerField(default=0)
    trial = models.ForeignKey(
        Trial,
        on_delete=models.CASCADE,
        default=None,
        null=True
    )
