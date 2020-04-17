import datetime

from django.http import HttpResponse

import main.forms as forms
import exceptions

from django.contrib.auth import login as log_user_in, logout as log_user_out
from django.contrib.auth.models import User
from main.views.form_view import FormView
from main.views.menu import get_menu_context, get_user_menu_context

from django.contrib.auth.decorators import login_required

import main.forms
from django.shortcuts import render, redirect
from main.db_tools.user_tools import DBUserTools
from django.contrib.auth.models import AnonymousUser


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
        ok, error = DBUserTools.try_register(login, password, email, team)
        if not ok:
            context["ok"] = False
            context["error"] = error
        else:
            context["success"] = True
            user = User.objects.get(username=login)
            log_user_in(request, user)
            context["user_menu"] = get_user_menu_context(user)


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


class ProfileFormPage(FormView):
    """**View-класс страницы '/profile/<int:uid>/'**\n
    Наследование от класса :class:`main.views.form_view.FormView`
    """
    pagename = "Профиль"
    form_class = forms.ProfileForm
    template_name = "pages/profile.html"

    @staticmethod
    def get_handler(context: dict, request, uid: int):
        """**Дополнительный обработчик post-запросов**\n
        Вызывается методом :meth:`main.views.form_view.FormView.get`

        :param context: контекст страницы
        :type context: dict
        :param request: запрос на страницу '/profile/<int:uid>/'
        :type request: HttpRequest
        :param uid: ID пользователя, которому принадлежат данные профиля
        :type uid: int
        """
        user = ProfileFormPage.__get_user(uid)
        context["self"] = ProfileFormPage.__does_profile_belong_to_current_user(request.user, uid)
        ProfileFormPage.__try_pull_user_data_to_context(user, context)

    @staticmethod
    def post_handler(context: dict, request, form, uid: int):
        """**Дополнительный обработчик post-запросов**\n
        Вызывается методом :meth:`main.views.form_view.FormView.post`

        :param context: контекст страницы
        :type context: dict
        :param request: запрос на страницу '/profile/<int:uid>/'
        :type request: HttpRequest
        :param form: форма, содержащая post-данные
        :type form: ProfileForm
        :param uid: ID пользователя, которому принадлежат данные профиля
        :type uid: int
        """
        self = context["self"] = ProfileFormPage.__does_profile_belong_to_current_user(request.user, uid)
        if not self:
            return HttpResponse(status_code=403)
        user = ProfileFormPage.__get_user(uid)
        ok, user_data = ProfileFormPage.__try_pull_user_data_to_context(user, context, return_user_data=True)
        if not ok:
            return
        action = form.data["action"]
        ProfileFormPage.__try_process_post_actions(action, context, form, user_data, user, request)
        if "del" in context:
            return redirect("/")

    @staticmethod
    def __get_user(uid: int) -> User:
        user, error = DBUserTools.try_find_user_with_id(uid)
        if user is None:
            raise Exception(error)
        return user

    @staticmethod
    def __does_profile_belong_to_current_user(req_user: User, uid: int) -> bool:
        return req_user.is_authenticated and (req_user.id == uid)

    @staticmethod
    def __try_pull_user_data_to_context(user: User, context: dict, return_user_data=False):
        user_data, error = DBUserTools.try_get_user_data(user)
        if error is not None:
            context["ok"] = False
            context["error"] = error
            return False, None if return_user_data else False
        context["login"] = user.username
        context["email"] = user.email
        context["regdate"] = user.date_joined
        context["victories"] = user_data.victories_count
        context["played_games"] = user_data.played_games_count
        context["activated"] = user_data.activated
        context["about"] = user_data.extra_info
        context["team"] = user_data.team
        context["exp"] = user_data.exp
        context["level"] = user_data.level
        context["reputation"] = user_data.reputation
        return True, user_data if return_user_data else True

    @staticmethod
    def __try_process_post_actions(action: str, context, form, user_data, user, request) -> bool:
        success = False
        error = None
        if action == "save-chan":  # сохранить изменения
            about = form.data["about"]
            user_data.extra_info = about
            user_data.save()
            success = True
        elif action == "save-pass":  # изменить пароль
            password = form.data["password"]
            if user.check_password(password):
                new_password = form.data["new_password"]
                if 0 < len(new_password) <= 64:
                    user.set_password(new_password)
                    user.save()
                    success = True
                    log_user_in(request, user)
                else:
                    error = "Длина пароля должна быть 1-64 символов!"
            else:
                error = "Текущий пароль не совпадает с указанным!"
        elif action == "del":  # удалить аккаунт
            log_user_out(request)
            DBUserTools.delete_user(user)
            context["del"] = success = True
        else:
            error = "Неверный формат отосланных данных!"
        context["ok"] = context["success"] = success
        context["error"] = error
        return success
