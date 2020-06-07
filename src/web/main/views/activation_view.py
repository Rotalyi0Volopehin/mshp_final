""" Страница активации почты юзера """

from django.contrib.auth.models import User
from django.contrib.auth import login
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import render

from main.db_tools.tokens import account_activation_token
from main.db_tools.user_tools import DBUserTools

from .menu import get_menu_context, get_user_menu_context


def activate(request, uid, token):
    """**View-функция страницы чата**

    :param request: request на страницу активации почты
    :type request: HttpRequest
    :param uid: ID пользователя
    :type uid: int
    :param token: токен активации почты
    :type token: string
    :return: response
    :rtype: HttpResponse
    """
    if request.method == "GET":
        context = {
            "pagename": "Верификация",
            "menu": get_menu_context(),
            "user_menu": get_user_menu_context(request.user)
        }
        try:
            uid = force_text(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            if DBUserTools.try_activate_user(user):
                login(request, user)
            context["error"] = 'Ссылка для верификации невалидна!'
        return render(request, 'registration/activation.html', context)
