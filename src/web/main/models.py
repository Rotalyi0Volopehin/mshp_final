# -*- coding: utf-8 -*-
import exceptions
import sys
import os
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from permalinks.models import Permalinks
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
    title = models.TextField(default='')  # название; уникально
    phase = models.IntegerField(default=0)  # фаза; 0 -- набор игроков, 1 -- основные действия, 2 -- readonly
    date_created = models.DateTimeField(default=timezone.now)  # дата вступления в фазу #0
    date_started = models.DateTimeField(default=timezone.now)  # дата вступления в фазу #1
    date_stopped = models.DateTimeField(default=timezone.now)  # дата вступления в фазу #2
    turn_of_team = models.IntegerField(default=0)  # фракция, совершающая ход
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


class TeamStats(models.Model):
    team = models.IntegerField(default=0)
    game_session = models.ForeignKey(to=GameSession, on_delete=models.CASCADE)
    money = models.IntegerField(default=0)  # бюджет фракции


class UserParticipation(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    user_data = models.ForeignKey(to=UserData, on_delete=models.CASCADE)
    game_session = models.ForeignKey(to=GameSession, on_delete=models.CASCADE)


class ChatManager(models.Manager):
    use_for_related_fields = True

    def unreaded(self, user=None):
        qs = self.get_queryset().exclude(last_message__isnull=True).filter(last_message__is_readed=False)
        return qs.exclude(last_message__author=user) if user else qs


class Chat(models.Model):
    DIALOG = 'D'
    CHAT = 'C'
    CHAT_TYPE_CHOICES = (
        (DIALOG, _('Dialog')),
        (CHAT, _('Chat'))
    )

    type = models.CharField(
        _('Тип'),
        max_length=1,
        choices=CHAT_TYPE_CHOICES,
        default=DIALOG
    )
    members = models.ManyToManyField(User, verbose_name=_("Участник"))

    last_message = models.ForeignKey('Message', related_name='last_message', null=True, blank=True,
                                     on_delete=models.SET_NULL)
    objects = ChatManager()

    @Permalinks
    def get_absolute_url(self):
        return reverse('users:messages', (), {'chat_id': self.pk})


class Message(models.Model):
    chat = models.ForeignKey(Chat, verbose_name=_("Чат"), on_delete=models.CASCADE)
    author = models.ForeignKey(User, verbose_name=_("Пользователь"), on_delete=models.CASCADE)
    message = models.TextField(_("Сообщение"))
    pub_date = models.DateTimeField(_('Дата сообщения'), default=timezone.now)
    is_readed = models.BooleanField(_('Прочитано'), default=False)
    class Meta:
        ordering = ['pub_date']

    def __str__(self):
        return self.message