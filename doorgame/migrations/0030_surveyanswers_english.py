# Generated by Django 2.2.18 on 2021-04-05 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doorgame', '0029_memorygamehighprelim_trialprelim'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveyanswers',
            name='english',
            field=models.TextField(default='blank'),
        ),
    ]
