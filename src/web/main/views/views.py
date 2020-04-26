from django.http import HttpResponse
from django.shortcuts import render
from main.views.menu import get_menu_context, get_user_menu_context


def index_page(request):
    """**View-функция страницы '/'**

    :param request: request на страницу '/'
    :type request: HttpRequest
    :return: response
    :rtype: HttpResponse
    """
    context = {
        'pagename': 'Главная',
        'author': 'Andrew',
        'pages': 4,
        'menu': get_menu_context(),
        'user_menu': get_user_menu_context(request.user),
    }
    return render(request, 'pages/index.html', context)


def darknet_page(request):
    context = {
        'pagename': 'DarkNet',
        'menu': get_menu_context(),
        'user_menu': get_user_menu_context(request.user),
    }
    return render(request, 'pages/darknet.html', context)


def forum_page(request):
    context = {
        'pagename': 'Форум',
        'menu': get_menu_context(),
        'user_menu': get_user_menu_context(request.user),
    }
    return render(request, 'pages/forum.html', context)


def chat_page(request):
    context = {
        'pagename': 'Закрытые каналы',
        'menu': get_menu_context(),
        'user_menu': get_user_menu_context(request.user),
    }
    return render(request, 'pages/chat.html', context)
