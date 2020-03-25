import exceptions
import net_connection.json_serialize as json_ser

from .channel import Channel
from net_connection.parcel_check import is_request_parcel_valid
from net_connection.parcel_check import is_response_parcel_valid


class ParcelManager:
    @staticmethod
    def send_parcel(parcel: list):
        if not is_request_parcel_valid(parcel):
            raise exceptions.ArgumentValueException()
        text_data = json_ser.CoreJSONEncoder().encode(parcel)
        Channel.send(text_data)

    @staticmethod
    def receive_parcel_now() -> list:
        response = Channel.receive_now()
        return ParcelManager.__convert_response_into_parcel(response)

    @staticmethod
    def receive_parcel_async(parcel_handler):
        if type(parcel_handler).__name__ != "function":
            raise exceptions.ArgumentTypeException()

        def receive_handler(response):
            parcel = ParcelManager.__convert_response_into_parcel(response)
            parcel_handler(parcel)
        Channel.receive_async(receive_handler)

    @staticmethod
    def __convert_response_into_parcel(response: str) -> list:
        parcel = json_ser.CoreJSONDecoder.decode_json(response)
        if not is_response_parcel_valid(parcel):
            raise Exception("Incorrect format of response parcel!")
        return parcel
