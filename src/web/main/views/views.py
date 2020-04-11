import datetime
import main.forms as forms
import exceptions

from django.shortcuts import render
from main.views.form_view import FormView
from main.views.menu import get_menu_context
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
    }
    return render(request, 'pages/time.html', context)


class RegistrationFormPage(FormView):
    """**View-класс страницы '/registration/'**\n
    Наследование от класса :class:`main.views.form_view.FormView`

    """

    pagename = "Регистрация"
    form_class = forms.RegistrationForm
    template_name = "registration/registration.html"

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
        login_ = form.data["login"]
        email = form.data["email"]
        team = int(form.data["team"])
        try:
            ok, error = DBUserTools.try_register(login_, password, email, team)
            if not ok:
                context["ok"] = False
                context["error"] = error
            else:
                context["success"] = True
        except exceptions.ArgumentValueException as exception:
            context["ok"] = False
            context["error"] = str(exception)
