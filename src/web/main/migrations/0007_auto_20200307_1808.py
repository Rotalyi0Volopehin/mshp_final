# Generated by Django 3.0.1 on 2020-03-07 15:08

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0006_auto_20200307_1807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamesession',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 7, 18, 8, 4, 880734)),
        ),
        migrations.AlterField(
            model_name='gamesession',
            name='date_started',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 7, 18, 8, 4, 880734)),
        ),
        migrations.AlterField(
            model_name='gamesession',
            name='date_stopped',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 7, 18, 8, 4, 880734)),
        ),
        migrations.CreateModel(
            name='UserStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coins', models.IntegerField(default=42)),
                ('income', models.IntegerField(default=1)),
                ('game_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.GameSession')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]