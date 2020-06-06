import exceptions

from enum import Enum
from net_connection.response_ids import ResponseID


class ErrorResponseID(Enum):
    INCORRECT_BYTE_DATA = 0  # если request - это bytes, но
    JSON_FORMAT_REQUIRED = 1  # если request - это string, но не json
    WRONG_PARCEL_FORMAT = 2  # если request - это не лист, пустой лист или первый элемент не request id
    WRONG_PARCEL_CONTENT = 3  # если содержание request parcel является неправильным
    LOGGING_IN_REQUIRED = 4  # если операция требует авторизации, но её не было
    INVALID_OPERATION = 5  # если операция не может быть произведена в данный момент


class ErrorResponse:
    def __init__(self, error_id: ErrorResponseID):  # никогда не исполняется
        pass

    @staticmethod
    def __arg_checker(error_id: ErrorResponseID) -> ErrorResponseID:
        if not isinstance(error_id, ErrorResponseID):
            raise exceptions.ArgumentTypeException()
        return error_id

    def __new__(cls, *args, **kwargs):  # возвращает parcel, содержащий error response
        error_id = ErrorResponse.__arg_checker(*args, **kwargs)
        return [ResponseID.ERROR, error_id]
