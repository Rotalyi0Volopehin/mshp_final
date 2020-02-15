import datetime

from django.contrib.auth.models import User
from django.contrib.auth.models import AnonymousUser
from django.db import models


# TODO: to document all these models


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
    team = models.IntegerField(default=0) # фракция
    extra_info = models.TextField(default='')


class UserStats(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    coins = models.IntegerField(default=0)
    exp = models.IntegerField(default=0)


class PressureToolSet(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    type = models.TextField(default='') # имя класса, отнаследованного от базового PressureTool


class GameSession(models.Model):
    started = models.BooleanField(default=False)
    stopped = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=datetime.datetime.now())
    date_started = models.DateTimeField(default=datetime.datetime.now())
    date_stopped = models.DateTimeField(default=datetime.datetime.now())
    turn_period = models.IntegerField(default=0) # период времени, выделенный под ход одной фракции
    team_count = models.IntegerField(default=0)
    user_lowest_level = models.IntegerField(default=-1) # нижний предел уровня игроков; -1 -- без предела
    user_highest_level = models.IntegerField(default=-1) # верхний предел уровня игроков; -1 -- без предела
    winning_team = models.IntegerField(default=-1) # победившая фракция; -1 -- неизвестно/ничья
    # путь до файла сессии должен быть "GameSessions\{id}_gs"


class GameSessionInvolvementFact(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    game_session = models.ForeignKey(to=GameSession, on_delete=models.CASCADE)