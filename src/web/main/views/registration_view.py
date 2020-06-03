""" Страница регистрации"""
from django.contrib.auth import login as log_user_in
from django.contrib.auth.models import User

import main.forms as forms
from main.db_tools.user_tools import DBUserTools
from main.views.form_view import FormView
from main.views.menu import get_user_menu_context


class RegistrationFormPage(FormView):
    """**View-класс страницы '/registration/'**\n
    Наследование от класса :class:`main.views.form_view.FormView`
    """
    pagename = "Регистрация"
    form_class = forms.RegistrationForm
    template_name = "registration/registration.html"

    @staticmethod
    def post_handler(context: dict, request, form):
        """**Дополнительный обработчик post-запросов**\n
        Вызывается методом :meth:`main.views.form_view.FormView.post`

        :param context: контекст страницы
        :type context: dict
        :param request: запрос на страницу '/registration/'
        :type request: HttpRequest
        :param form: форма, содержащая post-данные
        :type form: RegistrationForm
        """
        password = form.data["password1"]
        login = form.data["login"]
        email = form.data["email"]
        team = int(form.data["team"])
        okay, error = DBUserTools.try_register(login, password, email, team, request)
        if not okay:
            context["ok"] = False
            context["error"] = error
        else:
            context["success"] = True
            user = User.objects.get(username=login)
            log_user_in(request, user)
            context["user_menu"] = get_user_menu_context(user)
