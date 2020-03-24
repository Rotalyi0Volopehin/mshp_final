import exceptions

from net_connection.request_ids import RequestID


class RequestParcelHandlers:
    _handlers = {}

    @staticmethod
    def register_handler(handler, request_id: RequestID):
        if not (isinstance(request_id, RequestID) and (type(handler).__name__ == "function")):
            raise exceptions.ArgumentTypeException()
        if request_id in RequestParcelHandlers._handlers:
            err_msg = "Request parcel handler for specified request id already exists!"
            raise exceptions.InvalidOperationException(err_msg)
        RequestParcelHandlers._handlers[request_id] = handler
        return handler
