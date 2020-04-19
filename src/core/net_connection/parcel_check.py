from net_connection.request_ids import RequestID
from net_connection.response_ids import ResponseID


def is_request_parcel_valid(parcel):
    return isinstance(parcel, list) and (len(parcel) > 0) and isinstance(parcel[0], RequestID)


def is_response_parcel_valid(parcel):
    return isinstance(parcel, list) and (len(parcel) > 0) and isinstance(parcel[0], ResponseID)
