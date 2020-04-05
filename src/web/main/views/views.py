import datetime
import main.forms as forms
import exceptions

from django.shortcuts import render
from main.views.form_view import FormView
from main.views.menu import get_menu_context
from main.db_tools.user_tools import DBUserTools, is_email_valid


def index_page(request):
    context = {
        'pagename': 'Главная',
        'author': 'Andrew',
        'pages': 4,
        'menu': get_menu_context(),
    }
    return render(request, 'pages/index.html', context)


def time_page(request):
    context = {
        'pagename': 'Текущее время',
        'time': datetime.datetime.now().time(),
        'menu': get_menu_context(),
    }
    return render(request, 'pages/time.html', context)


class RegistrationFormPage(FormView):
    pagename = "Регистрация"
    form_class = forms.RegistrationForm
    template_name = "registration/registration.html"

    def post_handler(self, context: dict, request, form):
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
