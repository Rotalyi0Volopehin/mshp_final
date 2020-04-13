import datetime

from django.http import HttpResponse

import main.forms as forms
import exceptions

from django.shortcuts import render
from django.contrib.auth import login as log_user_in, logout as log_user_out
from django.contrib.auth.models import User
from main.views.form_view import FormView
from main.views.menu import get_menu_context, get_user_menu_context
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


def time_page(request):
    """**View-функция страницы '/time/'**

    :param request: request на страницу '/time/'
    :type request: HttpRequest
    :return: response
    :rtype: HttpResponse
    """
    context = {
        'pagename': 'Текущее время',
        'time': datetime.datetime.now().time(),
        'menu': get_menu_context(),
        'user_menu': get_user_menu_context(request.user),
    }
    return render(request, 'pages/time.html', context)


def profile_page(request, uid):
    return HttpResponse("Your ID is " + str(uid))


class RegistrationFormPage(FormView):
    """**View-класс страницы '/registration/'**\n
    Наследование от класса :class:`main.views.form_view.FormView`

    """

    pagename = "Регистрация"
    form_class = forms.RegistrationForm
    template_name = "registration/registration.html"
    display_user_menu = False

    def post_handler(self, context: dict, request, form):
        """**Дополнительный обработчик post-запросов**\n
        Вызывается методом :meth:`main.views.form_view.FormView.post`

        :param context: контекст страницы
        :type context: dict
        :param request: запрос на страницу '/registration/'
        :type request: HttpRequest
        :param form: форма, содержащая post-данные
        """
        password = form.data["password1"]
        login = form.data["login"]
        email = form.data["email"]
        team = int(form.data["team"])
        try:
            ok, error = DBUserTools.try_register(login, password, email, team)
            if not ok:
                context["ok"] = False
                context["error"] = error
            else:
                context["success"] = True
                user = User.objects.get(username=login)
                log_user_in(request, user)
                context["user_menu"] = get_user_menu_context(user)
        except exceptions.ArgumentValueException as exception:
            context["ok"] = False
            context["error"] = str(exception)
