# Generated by Django 2.2.10 on 2020-04-05 22:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('doorgame', '0019_surveyanswers_best_strategy'),
    ]

    operations = [
        migrations.AddField(
            model_name='memorygame',
            name='number_of_trial',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='MemoryGameList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='memorygame',
            name='memory_game_list',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='doorgame.MemoryGameList'),
        ),
    ]
