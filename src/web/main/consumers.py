import json
import net_connection.error_response as err_resp

from channels.generic.websocket import WebsocketConsumer
from net_connection.json_serialize import CoreJSONDecoder


# TODO: задокументировать


class WebsocketRequestHandler(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        # vvv первоначальная проверка формата request-а vvv
        if not self.check_bytes_data_absence(bytes_data):
            return
        ok, parcel = self.try_parse_json_into_parcel(text_data)
        if not ok:
            return
        if not self.check_parcel_format(parcel):
            return
        # vvv делегирование к обработчикам request-ов в соответствии с id request-ов vvv
        pass

    def check_bytes_data_absence(self, bytes_data) -> bool:
        if bytes_data is not None:
            error_response = err_resp.compose_error_response_parcel(err_resp.ErrorResponseID.BYTE_FORMAT_NOT_SUPPORTED)
            self.send(json.dumps(error_response))
            return False
        return True

    def try_parse_json_into_parcel(self, possible_json) -> (bool, object):
        try:
            parcel = CoreJSONDecoder.decode_json(possible_json)
            return True, parcel
        except:
            error_response = err_resp.compose_error_response_parcel(err_resp.ErrorResponseID.JSON_FORMAT_REQUIRED)
            self.send(error_response)
            return False, None

    def check_parcel_format(self, parcel) -> bool:
        if not (isinstance(parcel, list) and (len(parcel) > 0) and isinstance(parcel[0], err_resp.ErrorResponseID)):
            error_response = err_resp.compose_error_response_parcel(err_resp.ErrorResponseID.WRONG_PARCEL_FORMAT)
            self.send(error_response)
            return False
        return True
