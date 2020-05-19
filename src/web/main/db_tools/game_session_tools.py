import main.models
import exceptions
import os

from main.db_tools.game_session_error_messages import DBGameSessionErrorMessages
from .game_session_participation_error_messages import DBGameSessionParticipationErrorMessages
from django.contrib.auth.models import User
from main.models import UserData, UserParticipation, GameSession


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
    def can_user_sign_up_for_session(correct_user, user_data, game_session) -> (bool, str):
        if not (isinstance(correct_user, User) and isinstance(user_data, UserData) and
                isinstance(game_session, GameSession)):
            raise exceptions.ArgumentTypeException()
        if user_data.user != correct_user:
            raise exceptions.ArgumentValueException()
        if game_session.phase != 0:
            return False, DBGameSessionParticipationErrorMessages.enrollment_closed
        if (user_data.level < game_session.user_lowest_level) or (user_data.level > game_session.user_highest_level):
            return False, DBGameSessionParticipationErrorMessages.invalid_user_level
        if len(UserParticipation.objects.filter(user=correct_user)) > 0:
            return False, DBGameSessionParticipationErrorMessages.user_already_participates
        if DBGameSessionTools.__count_free_participant_places(user_data, game_session) == 0:
            return False, DBGameSessionParticipationErrorMessages.places_for_team_participants_over
        return True, None

    @staticmethod
    def __count_free_participant_places(user_data, game_session):
        participants = UserParticipation.objects.filter(game_session=game_session)
        free_places = game_session.user_per_team_count
        for participant in participants:
            if participant.user_data.team == user_data.team:
                free_places -= 1
        return free_places

    @staticmethod
    def __create_session_file(session: main.models.GameSession):
        # TODO: проверить директорию по-умолчанию
        path = os.path.join("GameSessions", str(session.id) + ".gses")
        file = open(path, 'w')
        # TODO: написать создание объекта core.GameSession и вписать его данные в файл
        file.close()
