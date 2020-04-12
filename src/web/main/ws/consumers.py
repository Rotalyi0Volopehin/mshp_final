import net_connection.error_response as err_resp
import exceptions

from channels.generic.websocket import WebsocketConsumer
from net_connection.json_serialize import CoreJSONEncoder
from net_connection.json_serialize import CoreJSONDecoder
from .request_parcel_handlers import RequestParcelHandlers
from net_connection.response_ids import ResponseID
from net_connection.request_ids import RequestID
from net_connection.parcel_check import is_request_parcel_valid
from net_connection.parcel_check import is_response_parcel_valid


# TODO: задокументировать


class WebsocketRequestHandler(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, code):  # при отключении происходит logout игрока
        fake_parcel = [RequestID.LOGOUT]
        self.receive(text_data=CoreJSONEncoder().encode(fake_parcel))

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
        response = CoreJSONEncoder().encode(response_parcel)
        self.send(response)
        if exception is not None:
            raise exception

    def check_bytes_data_absence(self, bytes_data) -> bool:
        if bytes_data is not None:
            error_response = err_resp.ErrorResponse(err_resp.ErrorResponseID.BYTE_FORMAT_NOT_SUPPORTED)
            self.send(CoreJSONEncoder().encode(error_response))
            return False
        return True

    def try_parse_json_into_parcel(self, possible_json) -> (bool, object):  # (ok, parcel)
        try:
            parcel = CoreJSONDecoder.decode_json(possible_json)
            return True, parcel
        except:
            error_response = err_resp.ErrorResponse(err_resp.ErrorResponseID.JSON_FORMAT_REQUIRED)
            self.send(CoreJSONEncoder().encode(error_response))
            return False, None

    def check_parcel_format(self, parcel) -> bool:
        if not is_request_parcel_valid(parcel):
            error_response = err_resp.ErrorResponse(err_resp.ErrorResponseID.WRONG_PARCEL_FORMAT)
            self.send(CoreJSONEncoder().encode(error_response))
            return False
        return True

    def try_delegate_parcel(self, parcel: list) -> (Exception, list):  # (exception, response_parcel)
        request_id = parcel[0]
        if request_id not in RequestParcelHandlers._handlers:
            exception = exceptions.NotImplementedException("Request parcel handler is not implemented!")
            return exception, [ResponseID.FAIL]
        handler = RequestParcelHandlers._handlers[request_id]
        response_parcel = handler(self, parcel)
        if not is_response_parcel_valid(response_parcel):
            exception = exceptions.InvalidReturnException("Request parcel handler must return response parcel!")
            return exception, [ResponseID.FAIL]
        return None, response_parcel
