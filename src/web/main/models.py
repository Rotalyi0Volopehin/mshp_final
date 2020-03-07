import datetime

from django.contrib.auth.models import User
from django.db import models


# TODO: задокументировать модели


# class User:
    # first_name - имя
    # email - email
    # username - логин
    # password - хэш пароля
    # date_joined - дата регистрации


class UserData(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    activated = models.BooleanField(default=False)
    victories_count = models.IntegerField(default=0)
    played_games_count = models.IntegerField(default=0)
    team = models.IntegerField(default=0)  # фракция
    exp = models.IntegerField(default=0)
    extra_info = models.TextField(default='')


class PressureToolSet(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    type = models.TextField(default='')  # имя класса, отнаследованного от базового PressureTool


class GameSession(models.Model):
    title = models.TextField(default='')  # название; уникально
    phase = models.IntegerField(default=0)  # фаза; 0 -- набор игроков, 1 -- основные действия, 2 -- readonly
    date_created = models.DateTimeField(default=datetime.datetime.now())  # дата вступления в фазу #0
    date_started = models.DateTimeField(default=datetime.datetime.now())  # дата вступления в фазу #1
    date_stopped = models.DateTimeField(default=datetime.datetime.now())  # дата вступления в фазу #2
    turn_of_team = models.IntegerField(default=0)  # фракция, совершающая ход
    turn_period = models.IntegerField(default=0)  # период времени в секундах, выделенный под ход одной фракции
    user_lowest_level = models.IntegerField(default=-1)  # нижний предел уровня игроков; -1 -- без предела
    user_highest_level = models.IntegerField(default=-1)  # верхний предел уровня игроков; -1 -- без предела
    user_limit = models.IntegerField(default=3)  # лимит общего числа игроков сессии
    winning_team = models.IntegerField(default=-1)  # победившая фракция; -1 -- неизвестно/ничья
    # путь до файла сессии должен быть "GameSessions/{id}.gses"


class UserStats(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    game_session = models.ForeignKey(to=GameSession, on_delete=models.CASCADE)
    coins = models.IntegerField(default=42)
    income = models.IntegerField(default=1)
    # эти данные уникальны для пары игрок-сессия
    # для каждого игрока может быть не более одной такой сущности
    # игрок может участвовать не более, чем в одной, сессии за раз
