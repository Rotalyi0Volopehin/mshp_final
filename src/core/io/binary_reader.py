import exceptions

from struct import unpack
from io import BytesIO


class BinaryReader:
    def __init__(self, base_stream: BytesIO = None):
        if not (isinstance(base_stream, BytesIO) or (base_stream is None)):
            raise exceptions.ArgumentTypeException()
        self.__base_stream = BytesIO() if base_stream is None else base_stream
        self.__read_methods = {
            int: self.read_int,
            bool: self.read_bool,
            str: self.read_str,
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

    def read_int(self) -> int:
        """**Чтение Int32**\n
        Формат данных : [data<32bit>]

        :return: Int32
        :rtype: int
        """
        bin_ = self.__base_stream.read(4)
        return unpack('>I', bin_)[0]

    def read_byte(self) -> int:
        """**Чтение Int8**\n
        Формат данных : [data<8bit>]

        :return: Int8
        :rtype: int
        """
        bin_ = self.__base_stream.read(1)
        return unpack('B', bin_)[0]

    def read_bool(self) -> bool:
        """**Чтение Boolean**\n
        Формат данных : [data<8bit>]

        :return: Boolean
        :rtype: bool
        """
        return self.read_byte() != 0

    def read_chars(self, length: int) -> str:
        """**Чтение строки известной длины**\n
        Формат данных : [chars<bytes>]

        :param length: Длина строки
        :type length: int
        :return: Строка
        :rtype: str
        """
        bin_ = self.__base_stream.read(length)
        return bin_.decode()

    def read_str(self) -> str:
        """**Чтение строки**\n
        Формат данных : [length<32bit>][chars<bytes>]

        :return: Строка
        :rtype: str
        """
        length = self.read_int()
        return self.read_chars(length)

    def read_short_str(self) -> str:
        """**Чтение строки длиной до 255 элементов**\n
        Формат данных : [length<8bit>][chars<bytes>]

        :return: Строка
        :rtype: str
        """
        length = self.read_byte()
        return self.read_chars(length)

    def __get_read_method(self, data_type: type):
        if hasattr(data_type, "read"):
            def method():
                return data_type.read(stream=self)
            return method
        if data_type in self.__read_methods:
            return self.__read_methods[data_type]
        raise exceptions.ArgumentValueException()

    def read(self, data_type: type):
        """**Чтение данных**\n
        Поддерживает int, bool, str и любые типы, имеющие метод 'read',
        принимающий параметр 'stream' типа BinaryReader\n
        Формат данных : [data<data_type>]

        :param data_type: Поддерживаемый тип данных
        :type data_type: type
        :return: Прочитанные данные
        """
        return self.__get_read_method(data_type)()

    def __read_iterable(self, length: int, elem_type: type, lazy: bool):
        read_method = self.__get_read_method(elem_type)
        if lazy:
            for _ in range(length):
                yield read_method()
        else:
            data = length * [None]
            for i in range(length):
                data[i] = read_method()

    def read_iterable(self, elem_type: type, lazy: bool = False):
        """**Чтение последовательности однотипных данных**\n
        Формат данных : [length<32bit>][elem<elem_type>]*length

        :param elem_type: Тип данных, поддерживаемый методом read
        :type elem_type: type
        :param lazy: Факт ленивости
        :type lazy: bool
        :return: Последовательность однотипных данных
        :rtype: list или generator
        """
        length = self.read_int()
        if lazy:
            for elem in self.__read_iterable(length, elem_type, True):
                yield elem
        else:
            return self.__read_iterable(length, elem_type, False)

    def read_short_iterable(self, elem_type: type, lazy: bool = False):
        """**Чтение последовательности однотипных данных длиной до 255 элементов**\n
        Формат данных : [length<8bit>][elem<elem_type>]*length

        :param elem_type: Тип данных, поддерживаемый методом read
        :type elem_type: type
        :param lazy: Факт ленивости
        :type lazy: bool
        :return: Последовательность однотипных данных
        :rtype: list или generator
        """
        length = self.read_byte()
        if lazy:
            for elem in self.__read_iterable(length, elem_type, True):
                yield elem
        else:
            return self.__read_iterable(length, elem_type, False)
