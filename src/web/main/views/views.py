from main.db_tools.cad import CAD
from django.http import HttpResponse

from main.views.menu import get_menu_context, get_user_menu_context
from django.shortcuts import render


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


def cad_page(request):
    CAD.clear_all_data()
    return HttpResponse("SUCCESS! All data is cleared")


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


def sessions_page(request):
    context = {
        'pagename': 'Сессии',
        'menu': get_menu_context(),
        'user_menu': get_user_menu_context(request.user),

    }
    tmp1 = [1,2,3,4]
    tmp2 = ['a','b', 'c', 'd']
    context['tables'] = [tmp1, tmp2]
    return render(request, 'pages/sessions.html', context)