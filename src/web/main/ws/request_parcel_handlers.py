import exceptions

from net_connection.request_ids import RequestID
from types import FunctionType


class RequestParcelHandlers:
    handlers = {}

    @staticmethod
    def register_handler(handler, request_id: RequestID):
        if not (isinstance(request_id, RequestID) and isinstance(handler, FunctionType)):
            raise exceptions.ArgumentTypeException()
        if request_id in RequestParcelHandlers.handlers:
            err_msg = "Request parcel handler for specified request id already exists!"
            raise exceptions.InvalidOperationException(err_msg)
        RequestParcelHandlers.handlers[request_id] = handler
        return handler
