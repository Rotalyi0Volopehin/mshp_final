from enum import Enum


class ResponseID(Enum):
    SUCCESS = 0  # parcel[1] { response_id<ResponseID> }
    FAIL = 1  # parcel[1] { response_id<ResponseID> }
    ERROR = 2  # parcel[2] { response_id<ResponseID>, error_id<ErrorResponseID> }
    DATA = 3  # parcel[2] { response_id<ResponseID>, data<object> }
    DEFEATED = 4
