from enum import Enum


class RequestID(Enum):
    LOGIN = 0  # parcel[3] { request_id<RequestID>, login<str>, password<str> }
    LOGOUT = 1  # parcel[1] { request_id<RequestID> }
    GET_GS_INFO = 2  # parcel[1] { request_id<RequestID> }
    GET_GAME_MODEL = 3  # parcel[1] { request_id<RequestID> }
    POST_CHANGES = 4  # parcel[2] { request_id<RequestID>, changes<bytes> }
    GET_CHANGES = 5  # parcel[1] { request_id<RequestID> }
    GAIN_EXP = 6  # parcel[1] { request_id<RequestID>, value<int> }
