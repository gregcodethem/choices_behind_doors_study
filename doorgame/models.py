from django.db import models
from django.contrib.auth.models import User


class Trial(models.Model):
	user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        default=None,
        null=True
    )

class MemoryGame(models.Model):
	user = models.ForeignKey(
		User,
        on_delete=models.CASCADE,
        default=None,
        null=True
		)

class Choice(models.Model):
    door_number = models.IntegerField(default=0)
    trial = models.ForeignKey(
    	Trial,
    	on_delete=models.CASCADE,
        default=None,
        null=True
    )

class Result(models.Model):
	door_number = models.IntegerField(default=0)
