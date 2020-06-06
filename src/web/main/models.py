import exceptions
import sys
import os

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class UserData(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    activated = models.BooleanField(default=False)
    victories_count = models.IntegerField(default=0)
    played_games_count = models.IntegerField(default=0)
    team = models.IntegerField(default=0)  # фракция [0; 2]
    level = models.IntegerField(default=0)
    exp = models.IntegerField(default=0)
    total_exp = models.IntegerField(default=0)
    extra_info = models.TextField(default='')

    @property
    def victory_ratio(self) -> float:
        if self.played_games_count == 0:
            return 0.0
        return self.victories_count / self.played_games_count

    @property
    def exp_cap(self) -> int:
        return 1 << self.level

    @property
    def can_levelup(self) -> bool:
        return self.exp_cap >= self.exp

    def levelup(self):
        if not self.try_levelup():
            raise exceptions.InvalidOperationException()

    def try_levelup(self) -> bool:
        cap = self.exp_cap
        if self.exp < cap:
            return False
        self.exp -= cap
        self.level += 1
        return True

    def gain_exp(self, exp: int):
        if not isinstance(exp, int):
            raise exceptions.ArgumentTypeException()
        if exp < 0:
            raise exceptions.ArgumentValueException()
        self.exp += exp
        self.total_exp += exp
        while self.try_levelup():
            pass


class PressureToolSet(models.Model):
    user_data = models.ForeignKey(to=UserData, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    type = models.TextField(default='')  # имя класса, отнаследованного от базового PressureTool

    @property
    def user(self) -> User:
        return self.user_data.user


class GameSession(models.Model):
    """class GameSession"""
    title = models.TextField(default='')  # название; уникально
    phase = models.IntegerField(default=0)
    # фаза; 0 -- набор игроков, 1 -- основные действия, 2 -- readonly
    date_created = models.DateTimeField(default=timezone.now)  # дата вступления в фазу #0
    date_started = models.DateTimeField(default=timezone.now)  # дата вступления в фазу #1
    date_stopped = models.DateTimeField(default=timezone.now)  # дата вступления в фазу #2
    turn_period = models.IntegerField(default=0)  # период времени в секундах, выделенный под ход одного игрока
    user_lowest_level = models.IntegerField(default=-1)  # нижний предел уровня игроков; -1 -- без предела
    user_highest_level = models.IntegerField(default=0xFFFF)  # верхний предел уровня игроков; 0xFFFF -- без предела
    user_per_team_count = models.IntegerField(default=2)  # лимит числа представителей для каждой фракции
    money_limit = models.IntegerField(default=255)  # лимит бюджета фракций
    winning_team = models.IntegerField(default=-1)  # победившая фракция; -1 -- неизвестно/ничья

    @property
    def file_path(self) -> str:
        current_path = os.path.abspath(sys.modules[__name__].__file__)
        web_path = current_path[:current_path.find("web") + 4]
        return os.path.join(web_path, "game_models", "{:0>8x}.gam".format(self.id))

    def get_participants(self):
        return UserParticipation.objects.filter(game_session=self)

    @property
    def level_limits_as_string(self) -> str:
        level_limits = ""
        if self.user_lowest_level != -1:
            level_limits += f"от {self.user_lowest_level} "
        if self.user_highest_level != 0xFFFF:
            level_limits += f"до {self.user_highest_level}"
        if len(level_limits) == 0:
            level_limits = "нет"
        return level_limits

    @property
    def players_gathered(self) -> str:
        participant_count = len(self.get_participants())
        participant_required = self.user_per_team_count * 3
        return f"{participant_count} из {participant_required}"


class UserParticipation(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    user_data = models.ForeignKey(to=UserData, on_delete=models.CASCADE)
    game_session = models.ForeignKey(to=GameSession, on_delete=models.CASCADE)
