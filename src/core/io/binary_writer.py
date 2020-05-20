import exceptions

from struct import pack
from io import BytesIO


class BinaryWriter:
    def __init__(self, base_stream: BytesIO = None):
        if not (isinstance(base_stream, BytesIO) or (base_stream is None)):
            raise exceptions.ArgumentTypeException()
        self.__base_stream = BytesIO() if base_stream is None else base_stream
        self.__write_methods = {
            int: self.write_int,
            bool: self.write_byte,
            str: self.write_str,
        }

    @property
    def base_stream(self) -> BytesIO:
        """**Базовый поток бинарных данных**\n
        :return: Базовый поток
        :rtype: BytesIO
        """
        return self.__base_stream

    @property
    def position(self) -> int:
        """**Текущая позиция каретки записи**\n
        :return: Позиция каретки
        :rtype: int
        """
        return self.__base_stream.tell()

    def seek(self, pos: int):
        """**Перемещение каретки записи**\n
        :param pos: Новая позиция каретки
        :rtype: int
        """
        self.__base_stream.seek(pos)

    def write_int(self, data: int):
        """**Запись Int32**\n
        Формат данных : [data<32bit>]

        :param data: Int32
        :type data: int
        """
        bin_ = pack('>I', data)
        self.__base_stream.write(bin_)

    def write_byte(self, data: int):
        """**Запись Int8**\n
        Формат данных : [data<8bit>]

        :param data: Int8
        :type data: int
        """
        bin_ = pack('B', data)
        self.__base_stream.write(bin_)

    def write_bool(self, data: bool):
        """**Запись Boolean**\n
        Формат данных : [data<8bit>]

        :param data: Boolean
        :type data: bool
        """
        self.write_byte(data)

    def write_chars(self, data: str):
        """**Запись строки известной длины**\n
        Формат данных : [chars<bytes>]

        :param data: Строка
        :type data: str
        """
        bin_ = data.encode()
        self.__base_stream.write(bin_)

    def write_str(self, data: str):
        """**Запись строки**\n
        Формат данных : [length<32bit>][chars<bytes>]

        :param data: Строка
        :type data: str
        """
        self.write_int(len(data))
        self.write_chars(data)

    def write_short_str(self, data: str):
        """**Запись строки длиной до 255 элементов**\n
        Формат данных : [length<8bit>][chars<bytes>]

        :param data: Строка
        :type data: str
        """
        self.write_byte(len(data))
        self.write_chars(data)

    def __get_write_method(self, data_type):
        if hasattr(data_type, "write"):
            def method(data):
                data_type.write(stream=self, obj=data)
            return method
        if data_type in self.__base_stream:
            return self.__write_methods[data_type]
        raise exceptions.ArgumentTypeException()

    def write(self, data):
        """**Запись данных**\n
        Поддерживает int, bool, str и любые типы, имеющие статический метод 'write',
        принимающий параметры 'stream' типа BinaryWriter и 'obj' типа data_type\n
        Формат данных : [data<data_type>]

        :param data: Данные
        """
        self.__get_write_method(type(data))(data)

    def __write_iterable(self, iterable, elem_type: type):
        write_method = self.__get_write_method(elem_type)
        for elem in iterable:
            write_method(elem)

    def write_iterable(self, iterable, elem_type: type):
        """**Запись последовательности однотипных данных**\n
        Формат данных : [length<32bit>][elem<elem_type>]*length

        :param iterable: Последовательность однотипных данных
        :param elem_type: Тип данных, поддерживаемый методом write
        :type elem_type: type
        """
        self.write_int(len(iterable))
        self.__write_iterable(iterable, elem_type)

    def write_short_iterable(self, iterable, elem_type: type):
        """**Запись последовательности однотипных данных длиной до 255 элементов**\n
        Формат данных : [length<8bit>][elem<elem_type>]*length

        :param iterable: Последовательность однотипных данных
        :param elem_type: Тип данных, поддерживаемый методом write
        :type elem_type: type
        """
        self.write_byte(len(iterable))
        self.__write_iterable(iterable, elem_type)
