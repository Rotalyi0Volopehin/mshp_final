from django.contrib import auth

from main import forms
from main.db_tools.cad import CAD
from django.http import HttpResponse

from main.db_tools.user_tools import DBUserTools
from main.views.form_view import FormView
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


class LoginFormPage(FormView):

    pagename = "Вход"
    form_class = forms.LoginForm
    template_name = "registration/login.html"

    def LoginView(self, request, form):
        username = form.data["login"]
        password = form.data["password"]
        ok = DBUserTools.check_user_existence(username, password)
        if ok:
            auth.login(username, password)