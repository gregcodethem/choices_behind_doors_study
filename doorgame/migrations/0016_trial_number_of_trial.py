# Generated by Django 2.2.10 on 2020-03-28 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doorgame', '0015_memorygame_initial_or_final'),
    ]

    operations = [
        migrations.AddField(
            model_name='trial',
            name='number_of_trial',
            field=models.IntegerField(default=0),
        ),
    ]
