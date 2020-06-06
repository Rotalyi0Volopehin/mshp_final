import exceptions

from io import BytesIO


class BinaryStream:
    def __init__(self, base_stream: BytesIO = None, data: bytes = None):
        if not ((isinstance(base_stream, BytesIO) or (base_stream is None)) and
                (isinstance(data, bytes) or (data is None))):
            raise exceptions.ArgumentTypeException()
        self.__base_stream = BytesIO(data) if base_stream is None else base_stream

    @property
    def base_stream(self) -> BytesIO:
        """**Базовый поток бинарных данных**\n
        :return: Базовый поток
        :rtype: BytesIO
        """
        return self.__base_stream

    @property
    def position(self) -> int:
        """**Текущая позиция каретки чтения**\n
        :return: Позиция каретки
        :rtype: int
        """
        return self.__base_stream.tell()

    def seek(self, pos: int):
        """**Перемещение каретки чтения**\n
        :param pos: Новая позиция каретки
        :rtype: int
        """
        self.__base_stream.seek(pos)

    def to_bytes(self) -> bytes:
        """**Получение всех данных, хранящихся в буфере**\n
        :return: Все данные
        :rtype: bytes
        """
        return self.base_stream.getbuffer().tobytes()

    def __len__(self) -> int:
        """**Длина потока бинарных данных**\n
        :return: Длина потока
        :rtype: int
        """
        return len(self.base_stream.getbuffer())
