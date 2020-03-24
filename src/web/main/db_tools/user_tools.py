import main.models
import re
import datetime
import exceptions

from django.contrib.auth.models import User
from adventures_web.settings import AUTO_USER_ACTIVATION
from main.db_tools.user_error_messages import DBUserErrorMessages


# TODO: задокументировать код


class DBUserTools:
    # TODO: добавить механизм верификации пользователей
    @staticmethod  # инструмент записи в БД
    def try_register(login: str, password: str, email: str, team: int) -> (bool, str):
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
            return False, DBUserErrorMessages.login_is_already_in_use
        if len(User.objects.filter(email=email)) > 0:
            return False, DBUserErrorMessages.email_is_already_in_use
        # vvv запись в БД vvv
        user = User(username=login, email=email, date_joined=datetime.datetime.now())
        user.set_password(password)
        user.save()
        user_data = main.models.UserData(user=user, team=team)
        if AUTO_USER_ACTIVATION:
            user_data.activated = True
        else:
            pass  # здесь отсылается письмо с ссылкой для верификации
        user_data.save()
        user_stats = main.models.UserStats(user=user)
        user_stats.save()
        return True, None

    @staticmethod  # инструмент удаления из БД
    def delete_user(user: User):
        # vvv проверка аргумента vvv
        if not isinstance(user, User):
            raise exceptions.ArgumentTypeException()
        # vvv удаление из БД vvv
        user_data = main.models.UserData.objects.filter(user=user)
        if len(user_data) > 0:
            user_data.delete()
        user_stats = main.models.UserStats.objects.filter(user=user)
        if len(user_stats) > 0:
            user_stats.delete()
        user.delete()

    @staticmethod  # инструмент проверки валидности
    def is_user_configuration_correct(user: User) -> bool:
        # vvv проверка аргумента vvv
        if not isinstance(user, User):
            raise exceptions.ArgumentTypeException()
        # vvv проверка валидности vvv
        user_data = main.models.UserData.objects.filter(user=user)
        if len(user_data) != 1:
            return False
        user_stats = main.models.UserStats.objects.filter(user=user)
        return len(user_stats) == 1

    @staticmethod  # инструмент проверки существования пары логин-пароль
    def check_user_login_and_password(login: str, password: str) -> bool:
        # vvv проверка аргументов vvv
        if not (isinstance(login, str) and isinstance(password, str)):
            raise exceptions.ArgumentTypeException()
        # vvv проверка данных по БД vvv
        user = User.objects.filter(login=login)
        if len(user) != 1:
            return False
        user = user[0]
        return user.check_password(password)


__email_re = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")


def is_email_valid(email):
    return __email_re.match(email)
