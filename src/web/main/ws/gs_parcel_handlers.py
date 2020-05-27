from net_connection.error_response import ErrorResponse, ErrorResponseID
from channels.generic.websocket import WebsocketConsumer
from main.ws.request_parcel_handlers import RequestParcelHandlers
from net_connection.request_ids import RequestID
from net_connection.response_ids import ResponseID
from .logged_in_sockets import LoggedInSockets
from main.db_tools.user_participation_tools import DBUSerParticipationTools


class GSParcelHandlers:
    @staticmethod
    def handle_get_participation_status_request(socket: WebsocketConsumer, parcel: list):
        if len(parcel) != 1:
            return ErrorResponse(ErrorResponseID.WRONG_PARCEL_FORMAT)
        user = LoggedInSockets.get_user_of_socket(socket)
        if user is None:
            return ErrorResponse(ErrorResponseID.LOGGING_IN_REQUIRED)
        status = DBUSerParticipationTools.get_participation_status(user)
        return [ResponseID.SUCCESS, status]


RequestParcelHandlers.register_handler(GSParcelHandlers.handle_get_participation_status_request,
                                       RequestID.GET_PARTICIPATION_STATUS)
