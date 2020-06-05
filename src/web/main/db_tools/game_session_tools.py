import exceptions
import os

from struct import error as struct_error_type
from django.utils import timezone
from main.db_tools.game_session_error_messages import DBGameSessionErrorMessages
from .game_session_participation_error_messages import DBGameSessionParticipationErrorMessages
from .user_tools import DBUserTools
from django.contrib.auth.models import User
from main.models import UserData, UserParticipation, GameSession, TeamStats
from io_tools.binary_writer import BinaryWriter
from io_tools.binary_reader import BinaryReader
from game_eng.game_model import GameModel
from game_eng.team_ders.team_a import TeamA
from game_eng.team_ders.team_b import TeamB
from game_eng.team_ders.team_c import TeamC
from game_eng.player import Player


class DBGameSessionTools:
    """**Инструменты работы в БД с данными об игровых сессиях**
    """
    @staticmethod
    def try_create_new_session(title: str, turn_period: int, user_per_team: int, team_money_limit: int,
                               user_lowest_level: int, user_highest_level: int) -> (GameSession, str):
        """**Попытка создания новой игровой сессии**\n
        :raises ArgumentTypeException: |ArgumentTypeException|
        :raises ArgumentValueException: |ArgumentValueException|
        :param title: Название игровой сессии
        :type title: str
        :param turn_period: Период хода игрока
        :type turn_period: int
        :param user_per_team: Количества игроков от каждой фракции
        :type user_per_team: int
        :param team_money_limit: Лимит бюджета фракции
        :type team_money_limit: int
        :param user_lowest_level: Нижний предел уровня допускаемых игроков
        :type user_lowest_level: int
        :param user_highest_level: Верхний предел уровня допускаемых игроков
        :type user_highest_level: int
        :return: (game_session, error)
        :rtype: (None, str) или (GameSession, None)
        """
        # vvv первичная проверка аргументов vvv
        if not (isinstance(title, str) and isinstance(turn_period, int) and isinstance(user_per_team, int) and
                isinstance(team_money_limit, int) and isinstance(user_lowest_level, int) and
                isinstance(user_highest_level, int)):
            raise exceptions.ArgumentTypeException()
        if (turn_period < 0) or (user_per_team < 1) or (user_lowest_level > user_highest_level):
            raise exceptions.ArgumentValueException()
        if user_lowest_level > user_highest_level:
            raise exceptions.ArgumentValueException()
        # vvv проверка согласованности аргументов с данными БД vvv
        if len(GameSession.objects.filter(title=title)) > 0:
            return None, DBGameSessionErrorMessages.title_is_already_in_use
        # vvv запись в БД vvv
        session = GameSession(title=title, turn_period=turn_period, user_per_team_count=user_per_team,
                              user_lowest_level=user_lowest_level, user_highest_level=user_highest_level,
                              money_limit=team_money_limit)
        session.save()
        return session, None

    @staticmethod
    def can_user_take_part_in_session(correct_user, user_data, game_session) -> (bool, str):
        if not (isinstance(correct_user, User) and isinstance(user_data, UserData) and
                isinstance(game_session, GameSession)):
            raise exceptions.ArgumentTypeException()
        if user_data.user != correct_user:
            raise exceptions.ArgumentValueException()
        if game_session.phase != 0:
            return False, DBGameSessionParticipationErrorMessages.enrollment_closed
        if (user_data.level > game_session.user_highest_level) or (user_data.level < game_session.user_lowest_level):
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
    def start_session_active_phase(session: GameSession):
        """**Перевод игровой сессии в фазу #1**\n
        Сессия должна находиться в фазе #0!

        :raises ArgumentTypeException: |ArgumentTypeException|
        :raises InvalidOperationException: |InvalidOperationException|
        :param session: Игровая сессия, которую требуется перевести в фазу #1
        :type session: GameSession
        """
        if not isinstance(session, GameSession):
            raise exceptions.ArgumentTypeException()
        if session.phase != 0:
            raise exceptions.InvalidOperationException()
        game_model = DBGameSessionTools.__create_new_game_model(session)
        DBGameSessionTools.save_game_model(session, game_model)
        for i in range(3):
            TeamStats(team=i, game_session=session).save()
        session.phase = 1
        session.date_started = timezone.now()
        session.save()

    @staticmethod
    def __create_new_game_model(session: GameSession) -> GameModel:
        game = GameModel(session.title, session.turn_period, session.money_limit, 16, 16)
        TeamA(game)
        TeamB(game)
        TeamC(game)
        participations = UserParticipation.objects.filter(game_session=session)
        for participation in participations:
            user_data = participation.user_data
            team = game.teams[user_data.team]
            Player(user_data.user.id, user_data.user.username, team)
        return game

    @staticmethod
    def end_session_active_phase(session: GameSession):
        """**Переход игровой сессии в фазу #2**\n
        Сессия должна находиться в фазе #1!

        :raises ArgumentTypeException: |ArgumentTypeException|
        :raises InvalidOperationException: |InvalidOperationException|
        :param session: Игровая сессия, которую требуется перевести в фазу #1
        :type session: GameSession
        """
        if not isinstance(session, GameSession):
            raise exceptions.ArgumentTypeException()
        if session.phase != 1:
            raise exceptions.InvalidOperationException()
        session.winning_team = DBGameSessionTools.__get_winning_team(session)
        os.remove(session.file_path)
        TeamStats.objects.filter(game_session=session).delete()
        participations = UserParticipation.objects.filter(game_session=session)
        for participation in participations:
            victory = participation.user_data.team == session.winning_team
            DBUserTools.do_game_session_end_user_data_change(participation.user_data, victory)
        participations.delete()
        session.phase = 2
        session.date_stopped = timezone.now()
        session.save()

    @staticmethod
    def __get_winning_team(session: GameSession) -> int:
        game_model, error = DBGameSessionTools.try_load_game_model(session)
        if error is not None:
            for i in range(3):
                if not game_model.teams[i].defeated:
                    return i
        return -1

    @staticmethod
    def try_load_game_model(session: GameSession, return_stream: bool = False) -> (GameModel, str):
        if not isinstance(session, GameSession):
            raise exceptions.ArgumentTypeException()
        try:
            stream = BinaryReader.get_stream_of_file(session.file_path)
            if return_stream:
                return stream, None
            game_model = GameModel.read(stream)
            return game_model, None
        except FileNotFoundError:
            return None, DBGameSessionParticipationErrorMessages.gs_file_not_found
        except struct_error_type:
            return None, DBGameSessionParticipationErrorMessages.incorrect_gs_file_format

    @staticmethod
    def save_game_model(session: GameSession, game_model: GameModel):
        if not (isinstance(session, GameSession) and isinstance(game_model, (GameModel, BinaryWriter))):
            raise exceptions.ArgumentTypeException()
        if isinstance(game_model, GameModel):
            stream = BinaryWriter()
            GameModel.write(stream, game_model)
        else:
            stream = game_model
        stream.write_to_file(session.file_path)
