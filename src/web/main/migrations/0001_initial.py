# Generated by Django 3.0.5 on 2020-05-26 16:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GameSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(default='')),
                ('phase', models.IntegerField(default=0)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_started', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_stopped', models.DateTimeField(default=django.utils.timezone.now)),
                ('turn_of_team', models.IntegerField(default=0)),
                ('turn_period', models.IntegerField(default=0)),
                ('user_lowest_level', models.IntegerField(default=-1)),
                ('user_highest_level', models.IntegerField(default=-1)),
                ('user_per_team_count', models.IntegerField(default=2)),
                ('money_limit', models.IntegerField(default=255)),
                ('winning_team', models.IntegerField(default=-1)),
            ],
        ),
        migrations.CreateModel(
            name='UserData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activated', models.BooleanField(default=False)),
                ('victories_count', models.IntegerField(default=0)),
                ('played_games_count', models.IntegerField(default=0)),
                ('team', models.IntegerField(default=0)),
                ('level', models.IntegerField(default=0)),
                ('exp', models.IntegerField(default=0)),
                ('total_exp', models.IntegerField(default=0)),
                ('reputation', models.IntegerField(default=0)),
                ('extra_info', models.TextField(default='')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserParticipation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.GameSession')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('user_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.UserData')),
            ],
        ),
        migrations.CreateModel(
            name='TeamStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team', models.IntegerField(default=0)),
                ('coins', models.IntegerField(default=42)),
                ('game_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.GameSession')),
            ],
        ),
        migrations.CreateModel(
            name='PressureToolSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=0)),
                ('type', models.TextField(default='')),
                ('user_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.UserData')),
            ],
        ),
    ]
