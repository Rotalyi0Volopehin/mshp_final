"""Контекст для навигации сайта"""

import exceptions

from django.contrib.auth.models import User, AnonymousUser


def get_menu_context() -> list:
    """Генератор контекста навигационной панели\n
    :return: Контекст навигационной панели
    :rtype: list
    """
    return [
        {"url_name": "darknet", "name": "darknet"},
        {"url_name": "forum", "name": "форум"},
        {"url_name": "chat", "name": "чат"},
    ]


def get_user_menu_context(user: User) -> list:
    """Генератор контекста навигационной панели пользователя\n
    :param user: Пользователь, пославший запрос (request.user)
    :type user: User или AnonymousUser
    :return: Контекст навигационной панели пользователя
    :rtype: list
    """
    if not isinstance(user, User or AnonymousUser):
        raise exceptions.ArgumentTypeException()
    return [
        {"url_name": "sessions", "name": "Сессии"},
        {"url": f"/profile/{user.id}/", "name": "Профиль"},
        {"url_name": "create session", "name": "Создание сессии"},
        {"url_name": "logout", "name": "Выйти"},
    ] if user.is_authenticated else [
        {"url_name": "registration", "name": "Регистрация"},
        {"url_name": "login", "name": "Войти"},
    ]
