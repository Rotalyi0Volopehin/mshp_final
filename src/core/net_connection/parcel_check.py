from net_connection.request_ids import RequestID
from net_connection.response_ids import ResponseID
from io_tools.binary_reader import BinaryReader
from io_tools.binary_writer import BinaryWriter


def is_request_parcel_valid(parcel):
    return isinstance(parcel, list) and (len(parcel) > 0) and isinstance(parcel[0], RequestID)


def is_response_parcel_valid(parcel):
    return isinstance(parcel, list) and (len(parcel) > 0) and isinstance(parcel[0], ResponseID)


def is_parcel_binary(response_parcel) -> bool:
    return (len(response_parcel) == 2) and isinstance(response_parcel[1], (BinaryWriter, BinaryReader))
