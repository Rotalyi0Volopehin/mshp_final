import datetime

from django.contrib import auth
from django.http import HttpResponse

import main.forms as forms

from main.db_tools.cad import CAD
from django.http import HttpResponse
from django.contrib.auth import login as log_user_in, logout as log_user_out
from django.contrib.auth.models import User
from main.views.form_view import FormView
from main.views.menu import get_menu_context, get_user_menu_context
from django.shortcuts import render, redirect
from main.db_tools.user_tools import DBUserTools


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
    return render(request, 'pages/time.html', context)


def cad_page(request):
    CAD.clear_all_data()
    return HttpResponse("SUCCESS! All data is cleared")



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

