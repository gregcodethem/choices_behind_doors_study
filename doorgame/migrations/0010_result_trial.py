# Generated by Django 2.2.10 on 2020-03-08 22:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('doorgame', '0009_memorygame'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='trial',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='doorgame.Trial'),
        ),
    ]
