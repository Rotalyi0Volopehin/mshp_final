import exceptions
import net_connection.json_serialize as json_ser

from types import FunctionType, MethodType
from net_connection.parcel_check import is_request_parcel_valid, is_response_parcel_valid, is_parcel_binary
from .channel import Channel
from net_connection.response_ids import ResponseID
from io_tools.binary_reader import BinaryReader


class ParcelManager:
    @staticmethod
    def send_parcel(parcel: list):
        if not is_request_parcel_valid(parcel):
            raise exceptions.ArgumentValueException()
        data_to_send = ParcelManager.__convert_parcel_into_request(parcel)
        Channel.send(data_to_send)

    @staticmethod
    def __convert_parcel_into_request(request_parcel: list):
        if is_parcel_binary(request_parcel):
            request_id = request_parcel[0]
            stream = request_parcel[1]
            stream.write_byte(request_id.value)
            stream.seek(0)
            binary_data = stream.base_stream.read()
            return binary_data
        else:
            text_data = json_ser.CoreJSONEncoder().encode(request_parcel)
            return text_data

    @staticmethod
    def receive_parcel_now() -> list:
        response = Channel.receive_now()
        return ParcelManager.__convert_response_into_parcel(response)

    @staticmethod
    def receive_parcel_async(parcel_handler):
        if not isinstance(parcel_handler, (FunctionType, MethodType)):
            raise exceptions.ArgumentTypeException()

        def receive_handler(response):
            parcel = ParcelManager.__convert_response_into_parcel(response)
            parcel_handler(parcel)
        Channel.receive_async(receive_handler)

    @staticmethod
    def __convert_response_into_parcel(response) -> list:
        if isinstance(response, bytes):
            stream = BinaryReader(data=response)
            stream.seek(len(stream) - 1)
            response_id = ResponseID(stream.read_byte())
            stream.seek(0)
            stream.base_stream.truncate(len(stream) - 1)
            parcel = [response_id, stream]
        else:
            parcel = json_ser.CoreJSONDecoder.decode_json(response)
        if not is_response_parcel_valid(parcel):
            raise Exception("Incorrect format of response parcel!")
        if parcel[0] == ResponseID.ERROR:
            raise exceptions.ErrorResponseException(parcel[1])
        return parcel
