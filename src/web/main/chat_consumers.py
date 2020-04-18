import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import User

from main.models import Message, Chat
import datetime
import locale


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Подключение к комнате
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Выход из комнаты
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Получение сообщения от WebSocket (от клиента)
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        room_name = text_data_json['room_name']
        user_id = text_data_json['user_id']
        message = text_data_json['message']

        # In terminal: export LC_ALL="ru_RU.UTF-8"
        locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
        current_date = datetime.datetime.now()
        time = str(current_date.strftime("%H:%M"))
        date = str(current_date.strftime("%A (%d.%m.%Y)"))

        user = None
        try:
            user = User.objects.filter(id=user_id).first()
        except User.DoesNotExist:
            pass

        # Сохранение в БД
        if user is not None:
            chat = Chat.objects.filter(name=room_name).first()
            if chat is not None:
                entry = Message(chat=chat, sender=user, text=message)
                entry.save()

        # Отправка сообщения в комнату
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'user_id': user_id,
                'message': message,
                'time': time,
                'date': date
            }
        )

    # Получение сообщение из комнаты (от сервера)
    def chat_message(self, event):
        user_id = event['user_id']
        message = event['message']
        time = event['time']
        date = event['date']

        # Отпраквка сообщения по WebSocket
        self.send(text_data=json.dumps({
            'user_id': user_id,
            'message': message,
            'time': time,
            'date': date
        }))
