import datetime
import main.forms as forms
from django.db.models import Count
from django.urls import reverse
from django.views import View
from django.contrib.auth import login as log_user_in

from main.db_tools.cad import CAD
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from main.views.menu import get_menu_context, get_user_menu_context
from main import forms
from main.db_tools.cad import CAD
from main.db_tools.user_tools import DBUserTools
from main.views.form_view import FormView
from main.models import Chat ,Message

def get_menu_context():
    return [
        {'url_name': 'index', 'name': 'Главная'},
        {'url_name': 'darknet', 'name': 'DarkNet'},
        {'url_name': 'forum', 'name': 'Форум'},
        {'url_name': 'chat', 'name': 'Закрытые каналы'},
        {'url_name': 'profile', 'name': 'Профиль'}

    ]


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


def forum_page(request):
    context = {
        'pagename': 'Форум',
        'menu': get_menu_context(),
        'user_menu': get_user_menu_context(request.user),
    }
    return render(request, 'pages/forum.html', context)




class LoginFormPage(FormView):

    pagename = "Вход"
    form_class = forms.LoginForm
    template_name = "registration/login.html"

    @staticmethod
    def post_handler(request, form):
        username = form.data["login"]
        password = form.data["password"]
        okay = DBUserTools.check_user_existence(username, password)
        if okay:
            user = User.objects.get(username=username)
            log_user_in(request, user)
            return redirect('/')
