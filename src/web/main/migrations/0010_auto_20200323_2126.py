# Generated by Django 3.0.1 on 2020-03-23 18:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20200307_1808'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamesession',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 23, 21, 26, 15, 23529)),
        ),
        migrations.AlterField(
            model_name='gamesession',
            name='date_started',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 23, 21, 26, 15, 23529)),
        ),
        migrations.AlterField(
            model_name='gamesession',
            name='date_stopped',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 23, 21, 26, 15, 23529)),
        ),
    ]