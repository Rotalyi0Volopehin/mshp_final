import locale
import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from main.models import Chat, Message
import hashlib

from main.views.menu import get_menu_context


def error(request, msg):
    context = {
        'pagename': 'Ошибка',
        'menu': get_menu_context(),
        'error': msg
    }
    return render(request, 'chat/error.html', context)


@login_required
def chats_list(request):
    context = {
        'pagename': 'Список чатов',
        'menu': get_menu_context()
    }

    chats = Chat.objects.all()
    chats = list(chats)
    if len(chats) > 0:
        for k in range(len(chats) - 1):
            for i in range(len(chats) - 1):
                last_msg_1 = Message.objects.filter(chat=chats[i]).last()
                last_msg_2 = Message.objects.filter(chat=chats[i + 1]).last()
                if (last_msg_1 is not None) and (last_msg_2 is not None):
                    if last_msg_1.date < last_msg_2.date:
                        chats[i], chats[i + 1] = chats[i + 1], chats[i]
                elif last_msg_2 is not None:
                    chats[i], chats[i + 1] = chats[i + 1], chats[i]
                # chats = sorted(chats, key=lambda k: Message.objects.filter(chat=k).last().date)
                # chats.reverse()
    my_chats = []
    for chat in chats:
        chat_members = list(chat.members.all())
        if request.user in chat_members:
            last_message = Message.objects.filter(chat=chat).last()
            if last_message is None:
                text = 'Пустой диалог.'
                time = '--:--'
            else:
                text = last_message.sender.username + ': ' + last_message.text
                # In terminal: export LC_ALL="ru_RU.UTF-8"
                locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
                time = str(last_message.date.strftime("%H:%M | %A (%d.%m.%Y)"))
            members_username = ''
            for member in chat_members:
                if member != request.user:
                    members_username += ', ' + member.username
            members_username = members_username[2:]
            my_chats.append({'members_username': members_username, 'text': text, 'room_name': chat.name, 'time': time})

    context['chats'] = my_chats
    return render(request, 'chat/list.html', context)


@login_required
def room(request, room_name):
    context = {
        'pagename': 'Чат',
        'menu': get_menu_context()
    }

    chat = Chat.objects.filter(name=room_name).first()
    if chat is None:
        return error(request, 'Такого чата не существует!')

    chat_members = list(chat.members.all())
    if request.user not in chat_members:
        return error(request, 'У вас нет доступа к этому чату!')

    messages = Message.objects.filter(chat=chat)
    context['chat_messages'] = messages

    members_username = ''
    for member in chat_members:
        if member != request.user:
            members_username += ', ' + member.username
    context['members_username'] = members_username[2:]

    context['room_name'] = room_name
    return render(request, 'chat/room.html', context)


@login_required
def open_user_chat(request, user_id):
    interlocutor = User.objects.filter(id=user_id).first()
    if interlocutor is None:
        return error(request, 'Такого пользователя не существует!')

    chats = Chat.objects.all()
    for chat in chats:
        chat_members = list(chat.members.all())
        if len(chat_members) == 2:
            if (interlocutor in chat_members) and (request.user in chat_members):
                return redirect('/chat/room/' + chat.name + '/')

    entry = Chat()
    entry.save()
    entry.members.add(request.user)
    entry.members.add(interlocutor)

    new_room_name = hashlib.sha256()
    new_room_name.update(str.encode(str(entry.id)))
    new_room_name.update(str.encode(str(entry.members)))
    new_room_name.update(str.encode(str(entry.id)))
    entry.name = new_room_name.hexdigest()

    entry.save()
    return redirect('/chat/room/' + entry.name + '/')