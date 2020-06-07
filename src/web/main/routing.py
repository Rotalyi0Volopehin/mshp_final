"""Роутинг"""
from django.urls import path, re_path

from .ws import consumers
from . import chat_consumers

websocket_urlpatterns = [
    path('ws/', consumers.WebsocketRequestHandler),
    re_path(r'ws/chat/(?P<room_name>\w+)/$', chat_consumers.ChatConsumer),
]
