# Generated by Django 2.2.10 on 2020-03-31 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doorgame', '0018_surveyanswers_age'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveyanswers',
            name='best_strategy',
            field=models.TextField(default='blank'),
        ),
    ]