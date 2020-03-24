import exceptions

from enum import Enum
from net_connection.response_ids import ResponseID


class ErrorResponseID(Enum):
    BYTE_FORMAT_NOT_SUPPORTED = 0  # если формат request не string, а bytes
    JSON_FORMAT_REQUIRED = 1  # если request - это string, но не json


def compose_error_response_parcel(error_id: ErrorResponseID):
    if not isinstance(error_id, ErrorResponseID):
        raise exceptions.ArgumentTypeException()
    return [ResponseID.ERROR, error_id]
