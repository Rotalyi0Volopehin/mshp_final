# Generated by Django 3.0.1 on 2020-03-01 17:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20200301_2006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamesession',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 1, 20, 6, 6, 274552)),
        ),
        migrations.AlterField(
            model_name='gamesession',
            name='date_started',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 1, 20, 6, 6, 274608)),
        ),
        migrations.AlterField(
            model_name='gamesession',
            name='date_stopped',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 1, 20, 6, 6, 274653)),
        ),
    ]
