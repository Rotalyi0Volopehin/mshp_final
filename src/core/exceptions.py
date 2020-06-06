class ArgumentTypeException(Exception):
    DESCRIPTION = "Неверный тип переданного аргумента"


class ArgumentValueException(Exception):
    DESCRIPTION = "Значение переданного аргумента не соответсвует требованиям"


class ArgumentOutOfRangeException(Exception):
    DESCRIPTION = "Значение переданного аргумента не принадлежит множеству допустимых значений"


class InvalidOperationException(Exception):
    DESCRIPTION = "Недопустимая операция"


class NotImplementedException(Exception):
    DESCRIPTION = "Нет реализации"


class InvalidReturnException(Exception):
    DESCRIPTION = "Неверное возвращаемое значение вызываемой функции"


class ErrorResponseException(Exception):
    DESCRIPTION = "Серверу кажется, что клиент не прав"

    def __init__(self, error_id):
        if not isinstance(error_id, int):
            from net_connection.error_response import ErrorResponseID
            if not isinstance(error_id, ErrorResponseID):
                raise ArgumentTypeException()
            error_id = error_id.value
        super().__init__(f"ErrorResponse #{error_id}")


class CoreModuleHashOverlapException(Exception):
    DESCRIPTION = "Хэши модулей core накладываются!"


class CoreClassHashOverlapException(Exception):
    DESCRIPTION = "Хэши классов core накладываются!"
