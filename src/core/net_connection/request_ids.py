from enum import Enum


class RequestID(Enum):
    LOGIN = 0  # parcel[3] { request_id<RequestID>, login<str>, password<str> }
    LOGOUT = 1  # parcel[1] { request_id<RequestID> }
    GET_PARTICIPATION_STATUS = 2  # parcel[1] { request_id<RequestID> }
