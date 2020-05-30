from net_connection.error_response import ErrorResponse, ErrorResponseID
from channels.generic.websocket import WebsocketConsumer
from main.ws.request_parcel_handlers import RequestParcelHandlers
from net_connection.request_ids import RequestID
from net_connection.response_ids import ResponseID
from .logged_in_sockets import LoggedInSockets
from main.db_tools.user_participation_tools import DBUSerParticipationTools


class GSParcelHandlers:
    @staticmethod
    def handle_get_gs_info_request(socket: WebsocketConsumer, parcel: list):
        if len(parcel) != 1:
            return ErrorResponse(ErrorResponseID.WRONG_PARCEL_FORMAT)
        user = LoggedInSockets.get_user_of_socket(socket)
        if user is None:
            return ErrorResponse(ErrorResponseID.LOGGING_IN_REQUIRED)
        status, participation = DBUSerParticipationTools.get_participation_status(user, True)
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


RequestParcelHandlers.register_handler(GSParcelHandlers.handle_get_gs_info_request, RequestID.GET_GS_INFO)
