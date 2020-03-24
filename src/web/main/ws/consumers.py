import json
import net_connection.error_response as err_resp
import exceptions

from channels.generic.websocket import WebsocketConsumer
from net_connection.json_serialize import CoreJSONDecoder
from .request_parcel_handlers import RequestParcelHandlers
from net_connection.response_ids import ResponseID
from net_connection.request_ids import RequestID


# TODO: задокументировать


class WebsocketRequestHandler(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, code):  # при отключении происходит logout игрока
        self.receive(text_data=json.dumps(RequestID.LOGOUT))

    def receive(self, text_data=None, bytes_data=None):
        # vvv первоначальная проверка формата request-а vvv
        if not self.check_bytes_data_absence(bytes_data):
            return
        ok, parcel = self.try_parse_json_into_parcel(text_data)
        if not ok:
            return
        if not self.check_parcel_format(parcel):
            return
        # vvv делегирование к обработчикам (request parcel handler) request-ов в соответствии с id request-ов vvv
        exception, response_parcel = self.try_delegate_parcel(parcel)
        self.send(response_parcel)
        if exception is not None:
            raise exception

    def check_bytes_data_absence(self, bytes_data) -> bool:
        if bytes_data is not None:
            error_response = err_resp.ErrorResponse(err_resp.ErrorResponseID.BYTE_FORMAT_NOT_SUPPORTED)
            self.send(json.dumps(error_response))
            return False
        return True

    def try_parse_json_into_parcel(self, possible_json) -> (bool, object):  # (ok, parcel)
        try:
            parcel = CoreJSONDecoder.decode_json(possible_json)
            return True, parcel
        except:
            error_response = err_resp.ErrorResponse(err_resp.ErrorResponseID.JSON_FORMAT_REQUIRED)
            self.send(error_response)
            return False, None

    @staticmethod
    def __is_parcel_format_correct(parcel) -> bool:
        return isinstance(parcel, list) and (len(parcel) > 0) and isinstance(parcel[0], err_resp.ErrorResponseID)

    def check_parcel_format(self, parcel) -> bool:
        if not WebsocketRequestHandler.__is_parcel_format_correct(parcel):
            error_response = err_resp.ErrorResponse(err_resp.ErrorResponseID.WRONG_PARCEL_FORMAT)
            self.send(error_response)
            return False
        return True

    def try_delegate_parcel(self, parcel: list) -> (Exception, list):  # (exception, response_parcel)
        request_id = parcel[0]
        if request_id not in RequestParcelHandlers._handlers:
            exception = exceptions.NotImplementedException("Request parcel handler is not implemented!")
            return exception, [ResponseID.FAIL]
        response_parcel = RequestParcelHandlers._handlers[parcel]()
        if not WebsocketRequestHandler.__is_parcel_format_correct(response_parcel):
            exception = exceptions.InvalidReturnException("Request parcel handler must return response parcel!")
            return exception, [ResponseID.FAIL]
        return None, response_parcel
