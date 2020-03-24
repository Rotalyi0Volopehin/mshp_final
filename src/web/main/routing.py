from django.urls import path

from .ws import consumers

websocket_urlpatterns = [
    path('ws/', consumers.WebsocketRequestHandler),
]
