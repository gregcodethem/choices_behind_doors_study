from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hard_or_easy_dots = models.TextField(max_length=10, blank=True)
    low_medium_or_high_dots_setting = models.TextField(max_length=10, blank=True)
    prelim_completed = models.BooleanField(default=False)
    memory_game_list_created = models.BooleanField(default=False)
    trials_completed = models.IntegerField(default=0)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()



class SurveyAnswers(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        default=None,
        null=True
    )
    regret_value = models.IntegerField(default=0)
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



class MemoryGameList(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        default=None,
        null=True
    )


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
    number_of_trial = models.IntegerField(default=0)
    memory_game_list = models.ForeignKey(
        MemoryGameList,
        on_delete=models.CASCADE,
        default=None,
        null=True
    )

class MemoryGameHigh(MemoryGame):
    box_10 = models.BooleanField(default=False)
    box_11 = models.BooleanField(default=False)
    box_12 = models.BooleanField(default=False)
    box_13 = models.BooleanField(default=False)
    box_14 = models.BooleanField(default=False)
    box_15 = models.BooleanField(default=False)
    box_16 = models.BooleanField(default=False)




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

