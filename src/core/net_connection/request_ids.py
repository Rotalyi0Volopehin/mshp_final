from enum import Enum


# TODO: задокументировать


class RequestIDs(Enum):
    LOGIN = 0  # parcel[3] { request_id<int>, login<str>, password<str> }
    LOGOUT = 1  # parcel[1] { request_id<int> }
