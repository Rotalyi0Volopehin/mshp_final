import main.models
import exceptions
import os

from main.db_tools.game_session_error_messages import DBGameSessionErrorMessages


class DBGameSessionTools:
    """**Инструменты работы в БД с данными об игровых сессиях**
    """
    @staticmethod
    def try_create_new_session(title: str, turn_period: int, user_limit: int,
                               user_lowest_level: int, user_highest_level: int) -> (bool, str):
        """**Попытка создания новой игровой сессии**\n
        :raises ArgumentTypeException: |ArgumentTypeException|
        :raises ArgumentValueException: |ArgumentValueException|
        :param title: Название игровой сессии
        :type title: str
        :param turn_period: Период хода
        :type turn_period: int
        :param user_limit: Предел количества игроков
        :type user_limit: int
        :param user_lowest_level: Нижний предел уровня допускаемых игроков
        :type user_lowest_level: int
        :param user_highest_level: Верхний предел уровня допускаемых игроков
        :type user_highest_level: int
        :return: (ok, error)
        :rtype: (bool, str) или (bool, None)
        """
        # vvv первичная проверка аргументов vvv
        if not (isinstance(title, str) and isinstance(turn_period, int) and isinstance(user_limit, int) and
                isinstance(user_lowest_level, int) and isinstance(user_highest_level, int)):
            raise exceptions.ArgumentTypeException()
        if (turn_period < 0) or (user_limit < 3) or (user_lowest_level < 0) or (user_highest_level < 0):
            raise exceptions.ArgumentValueException()
        if user_lowest_level > user_highest_level:
            raise exceptions.ArgumentValueException()
        # vvv проверка согласованности аргументов с данными БД vvv
        if len(main.models.GameSession.objects.filter(title=title)) > 0:
            return False, DBGameSessionErrorMessages.title_is_already_in_use
        # vvv запись в БД vvv
        session = main.models.GameSession(title=title, turn_period=turn_period, user_limit=user_limit,
                                          user_lowest_level=user_lowest_level, user_highest_level=user_highest_level)
        session.save()
        DBGameSessionTools.__create_session_file(session)
        return True, None

    @staticmethod
    def __create_session_file(session: main.models.GameSession):
        # TODO: проверить директорию по-умолчанию
        path = os.path.join("GameSessions", str(session.id) + ".gses")
        file = open(path, 'w')
        # TODO: написать создание объекта core.GameSession и вписать его данные в файл
        file.close()
