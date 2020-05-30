import net_connection.error_response as err_resp
import exceptions

from channels.generic.websocket import WebsocketConsumer
from main.ws.request_parcel_handlers import RequestParcelHandlers
from net_connection.request_ids import RequestID
from net_connection.response_ids import ResponseID
from main.db_tools.user_tools import DBUserTools
from main.models import User


class LoggedInSockets:
    users_of_sockets = dict()

    @staticmethod
    def get_user_of_socket(socket: WebsocketConsumer) -> User:
        if not isinstance(socket, WebsocketConsumer):
            raise exceptions.ArgumentTypeException()
        if socket in LoggedInSockets.users_of_sockets:
            return LoggedInSockets.users_of_sockets[socket]
        return None

    @staticmethod
    def try_login_socket(socket: WebsocketConsumer, user_login: str, user_password: str) -> bool:
        if not (isinstance(socket, WebsocketConsumer) and
                isinstance(user_login, str) and isinstance(user_password, str)):
            raise exceptions.ArgumentTypeException()
        user_exists = DBUserTools.check_user_existence(user_login, user_password)
        if not user_exists:
            return False
        user = User.objects.get(username=user_login)
        if user in LoggedInSockets.users_of_sockets.values():
            return False
        LoggedInSockets.users_of_sockets[socket] = user
        return True

    @staticmethod
    def try_logout_socket(socket: WebsocketConsumer) -> bool:
        if not isinstance(socket, WebsocketConsumer):
            raise exceptions.ArgumentTypeException()
        if socket in LoggedInSockets.users_of_sockets:
            LoggedInSockets.users_of_sockets.pop(socket)
            return True
        return False


def __login_request_parcel_handler(socket: WebsocketConsumer, parcel: list):
    if not ((len(parcel) == 3) and isinstance(parcel[1], str) and isinstance(parcel[2], str)):
        return err_resp.ErrorResponse(err_resp.ErrorResponseID.WRONG_PARCEL_FORMAT)
    ok = LoggedInSockets.try_login_socket(socket, parcel[1], parcel[2])
    return [ResponseID.SUCCESS if ok else ResponseID.FAIL]


def __logout_request_parcel_handler(socket: WebsocketConsumer, parcel: list):
    if len(parcel) != 1:
        return err_resp.ErrorResponse(err_resp.ErrorResponseID.WRONG_PARCEL_FORMAT)
    ok = LoggedInSockets.try_logout_socket(socket)
    return [ResponseID.SUCCESS if ok else ResponseID.FAIL]


RequestParcelHandlers.register_handler(__login_request_parcel_handler, RequestID.LOGIN)
RequestParcelHandlers.register_handler(__logout_request_parcel_handler, RequestID.LOGOUT)
