from enum import Enum


# TODO: задокументировать


class ResponseIDs(Enum):
    SUCCESS = 0  # parcel[1] { response_id<int> }
    FAIL = 1  # parcel[1] { response_id<int> }
    ERROR = 2  # parcel[2] { response_id<int>, error_id<int> }
    DATA = 3  # parcel[2] { response_id<int>, data<object> }
