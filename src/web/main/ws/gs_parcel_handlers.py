import exceptions

from channels.generic.websocket import WebsocketConsumer
from net_connection.error_response import ErrorResponse, ErrorResponseID
from main.ws.request_parcel_handlers import RequestParcelHandlers
from net_connection.request_ids import RequestID
from net_connection.response_ids import ResponseID
from main.db_tools.user_participation_tools import DBUserParticipationTools
from main.db_tools.game_session_tools import DBGameSessionTools
from io_tools.binary_reader import BinaryReader
from io_tools.binary_writer import BinaryWriter
from game_eng.player_turn import PlayerTurn
from .logged_in_sockets import LoggedInSockets


class GSParcelHandlers:
    @staticmethod
    def __try_get_participation(socket):
        user = LoggedInSockets.get_user_of_socket(socket)
        if user is None:
            return ErrorResponse(ErrorResponseID.LOGGING_IN_REQUIRED), None
        participation = DBUserParticipationTools.get_user_participation(user)
        if (participation is None) or (participation.game_session.phase != 1):
            return ErrorResponse(ErrorResponseID.INVALID_OPERATION), None
        return None, participation

    @staticmethod
    def handle_get_gs_info_request(socket: WebsocketConsumer, parcel: list):
        if len(parcel) != 1:
            return ErrorResponse(ErrorResponseID.WRONG_PARCEL_FORMAT)
        user = LoggedInSockets.get_user_of_socket(socket)
        if user is None:
            return ErrorResponse(ErrorResponseID.LOGGING_IN_REQUIRED)
        status, participation = DBUserParticipationTools.get_participation_status(user, True)
        if participation is None:
            return [ResponseID.DATA, status]
        game_session = participation.game_session
        gathered_players_count = len(game_session.get_participants())
        players_must_participate = game_session.user_per_team_count * 3
        return [
            ResponseID.DATA,
            status,
            game_session.title,
            gathered_players_count,
            players_must_participate,
        ]

    @staticmethod
    def handle_get_game_model_request(socket: WebsocketConsumer, parcel: list):
        if len(parcel) != 1:
            return ErrorResponse(ErrorResponseID.WRONG_PARCEL_FORMAT)
        err_resp, participation = GSParcelHandlers.__try_get_participation(socket)
        if err_resp is not None:
            return err_resp
        stream, _ = DBGameSessionTools.try_load_game_model(participation.game_session, True)
        if stream is None:
            return [ResponseID.FAIL]
        return [ResponseID.DATA, stream]

    @staticmethod
    def handle_post_changes_request(socket: WebsocketConsumer, parcel: list):
        if (len(parcel) != 2) or not isinstance(parcel[1], BinaryReader):
            return ErrorResponse(ErrorResponseID.WRONG_PARCEL_FORMAT)
        err_resp, participation = GSParcelHandlers.__try_get_participation(socket)
        if err_resp is not None:
            return err_resp
        game_model, _ = DBGameSessionTools.try_load_game_model(participation.game_session)
        if game_model.turn_time_left < -1.0:
            return [ResponseID.FAIL]  # post timeout
        if game_model.current_player.id != participation.user.id:
            return [ResponseID.FAIL]  # post не в свой ход
        try:
            player_turn = PlayerTurn.read(parcel[1], game_model)
        except:
            return ErrorResponse(ErrorResponseID.INCORRECT_BYTE_DATA)
        try:
            player_turn.sync()
            game_model.current_player_turn = player_turn
            game_model.next_player_turn()
            DBGameSessionTools.save_game_model(participation.game_session, game_model)
        except exceptions.InvalidOperationException:
            return [ResponseID.FAIL]  # провал синхронизации
        return [ResponseID.SUCCESS]

    @staticmethod
    def handle_get_changes_request(socket: WebsocketConsumer, parcel: list):
        if len(parcel) != 1:
            return ErrorResponse(ErrorResponseID.WRONG_PARCEL_FORMAT)
        err_resp, participation = GSParcelHandlers.__try_get_participation(socket)
        if err_resp is not None:
            return err_resp
        game_model, _ = DBGameSessionTools.try_load_game_model(participation.game_session)
        stream = BinaryWriter()
        if game_model.turn_time_left < -2.0:  # post timeout
            game_model.next_player_turn()
            DBGameSessionTools.save_game_model(participation.game_session, game_model)
        if game_model.prev_player_turn is None:
            return [ResponseID.FAIL]  # предыдущего хода не было
        PlayerTurn.write(stream, game_model.prev_player_turn)
        stream.write_datetime(game_model.turn_beginning_time)
        return [ResponseID.DATA, stream]


RequestParcelHandlers.register_handler(
    GSParcelHandlers.handle_get_gs_info_request, RequestID.GET_GS_INFO)
RequestParcelHandlers.register_handler(
    GSParcelHandlers.handle_get_game_model_request, RequestID.GET_GAME_MODEL)
RequestParcelHandlers.register_handler(GSParcelHandlers.handle_post_changes_request, RequestID.POST_CHANGES)
RequestParcelHandlers.register_handler(GSParcelHandlers.handle_get_changes_request, RequestID.GET_CHANGES)
