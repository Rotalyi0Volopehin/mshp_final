# TODO: задокументировать типы


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
