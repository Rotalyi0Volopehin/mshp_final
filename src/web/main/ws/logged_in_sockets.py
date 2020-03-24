from main.ws.request_parcel_handlers import RequestParcelHandlers
from net_connection.request_ids import RequestID
from net_connection.response_ids import ResponseID


class LoggedInSockets:
    users_of_sockets = {}

    @staticmethod
    def try_login_socket(socket, user_login, user_password) -> list:
        return [ResponseID.FAIL]

    @staticmethod
    def try_logout_socket(socket) -> list:
        if socket in LoggedInSockets.users_of_sockets:
            LoggedInSockets.users_of_sockets.pop(socket)
            return [ResponseID.SUCCESS]
        return [ResponseID.FAIL]


def __login_request_parcel_handler(parcel):
    pass


def __logout_request_parcel_handler(parcel):
    pass


RequestParcelHandlers.register_handler(__login_request_parcel_handler, RequestID.LOGIN)
RequestParcelHandlers.register_handler(__logout_request_parcel_handler, RequestID.LOGOUT)
