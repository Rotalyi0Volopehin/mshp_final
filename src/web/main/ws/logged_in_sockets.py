import exceptions
from channels.generic.websocket import WebsocketConsumer
import net_connection.error_response as err_resp
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
    def try_login_socket(socket: WebsocketConsumer, user_login: str, user_password: str) -> int:
        if not (isinstance(socket, WebsocketConsumer) and
                isinstance(user_login, str) and isinstance(user_password, str)):
            raise exceptions.ArgumentTypeException()
        user_exists = DBUserTools.check_user_existence(user_login, user_password)
        if not user_exists:
            return 0
        user = User.objects.get(username=user_login)
        if user in LoggedInSockets.users_of_sockets.values():
            return 0
        LoggedInSockets.users_of_sockets[socket] = user
        return user.id

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
    uid = LoggedInSockets.try_login_socket(socket, parcel[1], parcel[2])
    if uid == 0:
        return [ResponseID.FAIL]
    return [ResponseID.SUCCESS, uid]


def __logout_request_parcel_handler(socket: WebsocketConsumer, parcel: list):
    if len(parcel) != 1:
        return err_resp.ErrorResponse(err_resp.ErrorResponseID.WRONG_PARCEL_FORMAT)
    okay = LoggedInSockets.try_logout_socket(socket)
    return [ResponseID.SUCCESS if okay else ResponseID.FAIL]


RequestParcelHandlers.register_handler(__login_request_parcel_handler, RequestID.LOGIN)
RequestParcelHandlers.register_handler(__logout_request_parcel_handler, RequestID.LOGOUT)
