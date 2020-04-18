import main.models
import re
import datetime
import exceptions

from django.contrib.auth.models import User
from network_confrontation_web.settings import AUTO_USER_ACTIVATION
from main.db_tools.user_error_messages import DBUserErrorMessages
from main.models import UserData
# vvv для системы верификации vvv
from main.db_tools.tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage


# TODO: задокументировать код


class DBUserTools:
    """**Инструменты работы в БД с данными о пользователях**
    """
    @staticmethod
    def deleted_user_name() -> str:
        """Особый логин, обозначающий удалённого пользователя
        """
        return "$_del"

    @staticmethod
    def try_register(login: str, password: str, email: str, team: int, request) -> (bool, str):
        """**Попытка регистрации пользователя**\n
        Пробует зарегистрировать пользователя.
        Когда регистрация удаётся, посылает на указанный адрес письмо с ссылкой для верификации.
        Если в модуле :mod:`network_confrontation_web.settings` флаг 'AUTO_USER_ACTIVATION' имеет значение True,
        пользователь верифицируется сразу, а письмо не посылается.\n
        !!!Механизм верификации пользователей не завершён!!!

        Возможные исключения:\n
        - *ArgumentTypeException*
        - *ArgumentValueException*

        :param login: Логин (1-64 символа)
        :type login: str
        :param password: Пароль (1-64 символа)
        :type password: str
        :param email: E-mail (корректный)
        :type email: str
        :param team: Номер фракции (0-2)
        :type team: int
        :param request: Запрос на регистрацию
        :type request: HttpRequest
        :return: (ok, error)
        :rtype: (bool, str) или (bool, None)
        """
        # vvv первичная проверка аргументов vvv
        if not (isinstance(login, str) and isinstance(password, str) and
                isinstance(email, str)) and isinstance(team, int):
            raise exceptions.ArgumentTypeException()
        if not ((0 < len(login) <= 64) and (0 < len(email) <= 64) and (0 < len(password) <= 64) and (0 <= team < 3)):
            raise exceptions.ArgumentValueException()
        if not is_email_valid(email):
            raise exceptions.ArgumentValueException("E-mail некорректен!")
        del_name = DBUserTools.deleted_user_name()
        if login == del_name:
            raise exceptions.ArgumentValueException(f"Логин не должен принимать значение '{del_name}'!")
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
            DBUserTools.__send_email_with_activation_link(user, request)
        user_data.save()
        return True, None

    @staticmethod
    def __send_email_with_activation_link(user, request):
        subject = "Верификация аккаунта онлайн голосований"
        current_site = get_current_site(request)
        token = account_activation_token.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        activation_link = f"{current_site}/activate/{uid}/{token}/"
        message = "Ссылка для верификации аккаунта:\n" + activation_link
        email = EmailMessage(subject, message, to=[user.email])
        email.send()

    @staticmethod
    def delete_user(user: User):
        """**Инструмент удаления пользователя из БД**

        Возможные исключения:\n
        - *ArgumentTypeException*

        :param user: Пользователь
        :type user: User
        """
        # vvv проверка аргумента vvv
        if not isinstance(user, User):
            raise exceptions.ArgumentTypeException()
        # vvv удаление из БД vvv
        user_data = main.models.UserData.objects.filter(user=user)
        if len(user_data) > 0:
            user_data.delete()
        user.delete()

    @staticmethod
    def is_user_configuration_correct(user: User) -> bool:
        """**Инструмент проверки валидности пользовательских данных**\n
        Проверяет факт наличия в БД ровно одной записи типа :class:`main.models.UserData`.

        Возможные исключения:\n
        - *ArgumentTypeException*

        :param user: Пользователь
        :type user: User
        :return: Факт валидности пользовательских данных
        :rtype: bool
        """
        # vvv проверка аргумента vvv
        if not isinstance(user, User):
            raise exceptions.ArgumentTypeException()
        # vvv проверка валидности vvv
        user_data = main.models.UserData.objects.filter(user=user)
        return len(user_data) == 1

    @staticmethod
    def try_find_user_with_id(uid: int) -> (User, str):
        user = User.objects.filter(id=uid)
        if len(user) == 0:
            return None, DBUserErrorMessages.not_found
        return user[0], None

    @staticmethod
    def try_get_user_data(user) -> (UserData, str):
        user_data = UserData.objects.filter(user=user)
        if len(user_data) != 1:
            return None, DBUserErrorMessages.invalid_user_configuration
        return user_data[0], None

    @staticmethod
    def check_user_existence(login: str, password: str) -> bool:
        """**Инструмент проверки существования пары логин-пароль**\n
        Возможные исключения:\n
        - *ArgumentTypeException*

        :param login: Логин
        :type login: str
        :param password: Пароль
        :type password: str
        :return: Факт существования пары логин-пароль
        :rtype: bool
        """
        # vvv проверка аргументов vvv
        if not (isinstance(login, str) and isinstance(password, str)):
            raise exceptions.ArgumentTypeException()
        # vvv проверка данных по БД vvv
        user = User.objects.filter(username=login)
        if len(user) != 1:
            return False
        user = user[0]
        return user.check_password(password)

    @staticmethod
    def try_activate_user(user) -> bool:
        """**Инструмент верификации пользователей**\n
        Возможные исключения:\n
        - *ArgumentTypeException*

        :param user: Пользователь, аккаунт которого нужно верифицировать
        :type user: User
        :return: ok
        :rtype: bool
        """
        if not isinstance(user, User):
            raise exceptions.ArgumentTypeException()
        user_data, _ = DBUserTools.try_get_user_data(user)
        if user_data is None:
            return False
        if not user_data.activated:
            user_data.activated = True
            user_data.save()
        return True


__email_re = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")


def is_email_valid(email: str) -> bool:
    """**Метод для проверки валидности E-mail адреса**\n
    Возможные исключения:\n
    - *ArgumentTypeException*

    :param email: E-mail
    :type email: str
    :return: Факт валидности E-mail адреса
    :rtype: bool
    """
    if not isinstance(email, str):
        raise exceptions.ArgumentTypeException()
    return __email_re.match(email)
