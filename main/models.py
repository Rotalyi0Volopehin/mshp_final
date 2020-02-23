# -*- coding: utf-8 -*-

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


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


    def get_absolute_url(self):
        return reverse('users:messages', (), {'chat_id': self.pk})


class Message(models.Model):
    chat = models.ForeignKey(Chat, verbose_name=_("Чат"))
    author = models.ForeignKey(User, verbose_name=_("Пользователь"))
    message = models.TextField(_("Сообщение"))
    pub_date = models.DateTimeField(_('Дата сообщения'), default=timezone.now)
    is_readed = models.BooleanField(_('Прочитано'), default=False)

    class Meta:
        ordering = ['pub_date']

    def __str__(self):
        return self.message