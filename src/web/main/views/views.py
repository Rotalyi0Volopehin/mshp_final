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

from django.contrib.auth.decorators import login_required

import main.forms
from django.shortcuts import render, redirect
from main.db_tools.user_tools import DBUserTools
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import login, logout


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


#def profile_page(request, uid):
#    return HttpResponse("Your ID is " + str(uid))


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


def darknet_page(request):
    context = {
        'pagename': 'DarkNet',
        'menu': get_menu_context()
    }
    return render(request, 'pages/darknet.html', context)


def forum_page(request):
    context = {
        'pagename': 'Форум',
        'menu': get_menu_context()
    }
    return render(request, 'pages/forum.html', context)


def chat_page(request):
    context = {
        'pagename': 'Закрытые каналы',
        'menu': get_menu_context()
    }
    return render(request, 'pages/chat.html', context)

def fraction1_page(request):
    context = {
        'pagename': 'Фракция1',
        'menu': get_menu_context()
    }
    return render(request, 'pages/fraction1.html', context)

def view_func_template(request, html_path, form_class, post_handler, get_handler=None, context=None):
    if context is None:
        context = {}
    context["menu"] = get_menu_context()
    success = ok = False
    error = None
    if request.method == "POST":
        form = form_class(request.POST)
        if form.is_valid():
            ok, error, success = post_handler(form=form, context=context)
        else:
            error = "Неверный формат отосланных данных!"
    else:
        if get_handler is None:
            form = form_class()
            ok = True
        else:
            ok, error, success, form = get_handler(context=context)
    context["form"] = form
    context["ok"] = ok
    context["error"] = error
    context["success"] = success
    return render(request, html_path, context)


def profile_page(request, id):
    context = {}
    def body(form=None, context=None):
        ok = success = False
        user, error = DBUserTools.try_find_user_with_id(id)
        if error is None:
            user_data, error = DBUserTools.try_get_user_data(user)
            if error is None:
                self = context['self'] = not isinstance(request.user, AnonymousUser) and (user.id == request.user.id)
                context['pagename'] = "Мой профиль" if self else "Профиль"
                if self and (form != None):
                    ok, error, success = post_handler(form, context, user, user_data)
                context['login'] = user.username
                context['email'] = user.email
                context['regdate'] = user.date_joined
                context['victories'] = user_data.victories_count
                context['played_games'] = user_data.played_games_count
                context['activated'] = user_data.activated
                context['about'] = user_data.extra_info
                context['team'] = user_data.team
                context['exp'] = user_data.exp
                context['level'] = user_data.level
                context['reputation'] = user_data.reputation

        else:
            context["pagename"] = "Профиль"
        result = [ok, error, success]
        if form is None:
            result.append(None)
        return result

    def post_handler(form, context, user, user_data):
        success = ferr = False
        error = None
        action = form.data["action"]
        if action == "save-chan":
            about = form.data["about"]
            user_data.extra_info = about
            user_data.save()
            success = True

        elif action == "save-pass":
            password = form.data["password"]
            if user.check_password(password):
                new_password = form.data["new_password"]
                if 0 < len(new_password) <= 64:
                    user.set_password(new_password)
                    user.save()
                    success = True
                else:
                    error = "Длина пароля должна быть больше 1, но меньше 65 символов!"
            else:
                error = "Текущий пароль не совпадает с указанным!"
        elif action == "del":
            logout(request)
            user.delete()
            context["del"] = success = True
        else:
            ferr = True
        if ferr:
            error = "Неверный формат отосланных данных!"
        return success, error, success
    result = view_func_template(request, "pages/profile.html", main.forms.ProfileForm, body, get_handler=body, context=context)
    return redirect("/") if "del" in context else result

@login_required
def my_profile_page(request):
    return profile_page(request, request.user.id)