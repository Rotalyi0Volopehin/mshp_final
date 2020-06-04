# -*- coding: utf-8 -*-

"""AppConfig"""
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _
from main.receivers import receiver


class MainConfig(AppConfig):
    """class MainConfig"""
    name = 'main'


class UsersConfig(AppConfig):
    name = 'users'
    verbose_name = _('Users')

    def ready(self):
        import users.receivers
