# Generated by Django 2.2.10 on 2020-03-08 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doorgame', '0007_auto_20200308_2106'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='door_number',
            field=models.IntegerField(default=0),
        ),
    ]
