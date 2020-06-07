""" Основные View функции сайта """

from django.contrib.auth import login as log_user_in
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from main.views.menu import get_menu_context, get_user_menu_context
from main import forms
from main.db_tools.user_tools import DBUserTools
from main.db_tools.user_error_messages import DBUserErrorMessages
from main.views.form_view import FormView


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


def chat_page(request):
    """**View-функция страницы чата**

    :param request: request на страницу '/chat/'
    :type request: HttpRequest
    :return: response
    :rtype: HttpResponse
    """
    context = {
        'pagename': 'Закрытые каналы',
        'menu': get_menu_context(),
        'user_menu': get_user_menu_context(request.user),
    }
    return render(request, 'pages/chat.html', context)


class LoginFormPage(FormView):
    """**Страница с формой авторизации**"""

    pagename = "Вход"
    form_class = forms.LoginForm
    template_name = "registration/login.html"

    @staticmethod
    def post_handler(context, request, form):
        """**Обработчик POST запроса на страницу**

        :param context: данные страницы
        :param request: request на страницу авторизации
        :type request: HttpRequest
        :param form: форма авторизации
        :type form: FormView
        :return: redirect
        :rtype: HttpResponseRedirect
        """
        username = form.data["login"]
        password = form.data["password"]
        exists = DBUserTools.check_user_existence(username, password)
        if exists:
            user = User.objects.get(username=username)
            log_user_in(request, user)
            return redirect('/')
        raise Exception(DBUserErrorMessages.not_found)
