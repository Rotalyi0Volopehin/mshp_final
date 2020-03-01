import datetime

from django.shortcuts import render


def get_menu_context():
    return [
        {'url_name': 'index', 'name': 'Главная'},
        {'url_name': 'darknet', 'name': 'DarkNet'},
        {'url_name': 'forum', 'name': 'Форум'},
        {'url_name': 'chat', 'name': 'Закрытые каналы'},
        {'url_name': 'profile', 'name': 'Профиль'}

    ]


def index_page(request):
    context = {
        'pagename': 'Главная',
        'author': 'Andrew',
        'pages': 4,
        'menu': get_menu_context()
    }
    return render(request, 'pages/index.html', context)


def darknet_page(request):
    context = {
        'pagename': 'DarkNet',
        'menu': get_menu_context()
    }
    return render(request, 'pages/darknet.html', context)


def forum_page(request):
    context = {
        'pagename': 'Форум',
        'menu': get_menu_context()
    }
    return render(request, 'pages/forum.html', context)


def chat_page(request):
    context = {
        'pagename': 'Закрытые каналы',
        'menu': get_menu_context()
    }
    return render(request, 'pages/chat.html', context)


def profile_page(request):
    context = {
        'pagename': 'Профиль',
        'menu': get_menu_context()
    }
    return render(request, 'pages/profile.html', context)
