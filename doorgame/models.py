from django.db import models

# Create your models here.
class Choice(models.Model):
	door_number = models.IntegerField(default=0)
