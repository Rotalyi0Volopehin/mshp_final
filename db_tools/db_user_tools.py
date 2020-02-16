import main.models
import exceptions
import re
import datetime

from django.contrib.auth.models import User
from simple_votings.settings import AUTO_USER_ACTIVATION


# TODO: задокументировать код


class DB_UserTools:
    # TODO: добавить механизм верификации пользователей
    @staticmethod # инструмент записи в БД
    def try_register(login, password, email, team) -> (bool, str):
        # vvv первичная проверка аргументов vvv
        if not (isinstance(login, str) and isinstance(password, str) and isinstance(email, str)) and isinstance(team, int):
            raise exceptions.ArgumentTypeException()
        if not ((0 < len(login) <= 64) and (0 < len(email) <= 64) and (0 < len(password) <= 64) and (0 <= team < 3)):
            raise exceptions.ArgumentValueException()
        if not is_email_valid(email):
            raise exceptions.ArgumentValueException("E-mail некорректен!")
        if login == "$_del":
            raise exceptions.ArgumentValueException("Логин не должен принимать значение '$_del'!")
        # vvv проверка согласованности аргументов с данными БД vvv
        if len(User.objects.filter(username=login)) > 0:
            return False, "Пользователь с данным логином уже существует!"
        if len(User.objects.filter(email=email)) > 0:
            return False, "Пользователь с указанным E-mail уже существует!"
        # vvv запись в БД vvv
        user = User(username=login, email=email, date_joined=datetime.datetime.now())
        user.set_password(password)
        user.save()
        user_data = main.models.UserData(user=user, team=team)
        if AUTO_USER_ACTIVATION:
            user_data.activated = True
        else:
            pass # здесь отсылается письмо с ссылкой для верификации
        user_data.save()
        user_stats = main.models.UserStats(user=user)
        user_stats.save()
        return True, None


__email_re = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")


def is_email_valid(email):
    return __email_re.match(email)