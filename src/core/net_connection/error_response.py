import exceptions

from enum import Enum
from net_connection.response_ids import ResponseID


# TODO: задокументировать


class ErrorResponseID(Enum):
    BYTE_FORMAT_NOT_SUPPORTED = 0  # если формат request не string, а bytes
    JSON_FORMAT_REQUIRED = 1  # если request - это string, но не json
    WRONG_PARCEL_FORMAT = 2  # если request - это не лист, пустой лист или первый элемент не request id


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
