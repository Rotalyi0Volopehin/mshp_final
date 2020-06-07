from channels.generic.websocket import WebsocketConsumer
from net_connection.error_response import ErrorResponse, ErrorResponseID
from main.ws.request_parcel_handlers import RequestParcelHandlers
from net_connection.request_ids import RequestID
from net_connection.response_ids import ResponseID
from .logged_in_sockets import LoggedInSockets
from main.db_tools.user_tools import DBUserTools


class UserManagementParcelHandler:
    @staticmethod
    def handle_gain_exp_request(socket: WebsocketConsumer, parcel: list):
        if len(parcel) != 2:
            return ErrorResponse(ErrorResponseID.WRONG_PARCEL_FORMAT)
        user = LoggedInSockets.get_user_of_socket(socket)
        if user is None:
            return ErrorResponse(ErrorResponseID.LOGGING_IN_REQUIRED), None
        user_data, error = DBUserTools.try_get_user_data(user)
        if user_data is None:
            return [ResponseID.FAIL]
        try:
            user_data.gain_exp(parcel[1])
        except:
            return ErrorResponse(ErrorResponseID.WRONG_PARCEL_CONTENT)
        user_data.save()
        return [ResponseID.SUCCESS]


RequestParcelHandlers.register_handler(UserManagementParcelHandler.handle_gain_exp_request, RequestID.GAIN_EXP)
