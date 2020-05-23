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
            str: self.read_string,
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
        return unpack('>i', bin_)[0]

    def read_uint(self) -> int:
        """**Чтение UnsignedInt32**\n
        Формат данных : [data<32bit>]

        :return: UnsignedInt32
        :rtype: int
        """
        bin_ = self.__base_stream.read(4)
        return unpack('>I', bin_)[0]

    def read_byte(self) -> int:
        """**Чтение UnsignedInt8**\n
        Формат данных : [data<8bit>]

        :return: UnsignedInt8
        :rtype: int
        """
        bin_ = self.__base_stream.read(1)
        return unpack('B', bin_)[0]

    def read_sbyte(self) -> int:
        """**Чтение Int8**\n
        Формат данных : [data<8bit>]

        :return: Int8
        :rtype: int
        """
        bin_ = self.__base_stream.read(1)
        return unpack('b', bin_)[0]

    def read_bool(self) -> bool:
        """**Чтение Boolean**\n
        Формат данных : [data<8bit>]

        :return: Boolean
        :rtype: bool
        """
        return self.read_byte() != 0

    def read_int_point(self) -> tuple:
        """**Чтение точки Int32**\n
        Формат данных : [x<32bit>][y<32bit>]

        :return: Точка Int32
        :rtype: (int, int)
        """
        x = self.read_int()
        y = self.read_int()
        return x, y

    def read_uint_point(self) -> tuple:
        """**Чтение точки UnsignedInt32**\n
        Формат данных : [x<32bit>][y<32bit>]

        :return: Точка UnsignedInt32
        :rtype: (int, int)
        """
        x = self.read_uint()
        y = self.read_uint()
        return x, y

    def read_byte_point(self) -> tuple:
        """**Чтение точки UnsignedInt8**\n
        Формат данных : [x<8bit>][y<8bit>]

        :return: Точка UnsignedInt8
        :rtype: (int, int)
        """
        x = self.read_byte()
        y = self.read_byte()
        return x, y

    def read_sbyte_point(self) -> tuple:
        """**Чтение точки Int8**\n
        Формат данных : [x<8bit>][y<8bit>]

        :return: Точка Int8
        :rtype: (int, int)
        """
        x = self.read_sbyte()
        y = self.read_sbyte()
        return x, y

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

    def read_string(self) -> str:
        """**Чтение строки**\n
        Формат данных : [length<32bit>][chars<bytes>]

        :return: Строка
        :rtype: str
        """
        length = self.read_uint()
        return self.read_chars(length)

    def read_short_string(self) -> str:
        """**Чтение строки длиной до 255 элементов**\n
        Формат данных : [length<8bit>][chars<bytes>]

        :return: Строка
        :rtype: str
        """
        length = self.read_byte()
        return self.read_chars(length)

    def __get_read_method(self, data_type: type, extra_kwargs: dict):
        if hasattr(data_type, "read"):
            if extra_kwargs is None:
                def method():
                    return data_type.read(stream=self)
            else:
                def method():
                    return data_type.read(stream=self, **extra_kwargs)
            return method
        if data_type in self.__read_methods:
            return self.__read_methods[data_type]
        raise exceptions.ArgumentValueException()

    def read(self, data_type: type, extra_kwargs: dict = None):
        """**Чтение данных**\n
        Поддерживает int, bool, str и любые типы, имеющие метод 'read',
        принимающий параметр 'stream' типа BinaryReader\n
        Формат данных : [data<data_type>]

        :param data_type: Поддерживаемый тип данных
        :type data_type: type
        :param extra_kwargs: kwargs для метода 'read' загружаемого типа
        :type extra_kwargs: dict
        :return: Прочитанные данные
        """
        return self.__get_read_method(data_type, extra_kwargs)()

    def __read_iterable(self, length: int, elem_type: type, lazy: bool, extra_kwargs: dict):
        read_method = self.__get_read_method(elem_type, extra_kwargs)
        if lazy:
            for _ in range(length):
                yield read_method()
        else:
            data = length * [None]
            for i in range(length):
                data[i] = read_method()

    def read_iterable(self, elem_type: type, lazy: bool = False, extra_kwargs: dict = None):
        """**Чтение последовательности однотипных данных**\n
        Формат данных : [length<32bit>][elem<elem_type>]*length

        :param elem_type: Тип данных, поддерживаемый методом read
        :type elem_type: type
        :param lazy: Факт ленивости
        :type lazy: bool
        :param extra_kwargs: kwargs для метода 'read' загружаемого типа
        :type extra_kwargs: dict
        :return: Последовательность однотипных данных
        :rtype: list или generator
        """
        length = self.read_uint()
        if lazy:
            for elem in self.__read_iterable(length, elem_type, True, extra_kwargs):
                yield elem
        else:
            return self.__read_iterable(length, elem_type, False, extra_kwargs)

    def read_short_iterable(self, elem_type: type, lazy: bool = False, extra_kwargs: dict = None):
        """**Чтение последовательности однотипных данных длиной до 255 элементов**\n
        Формат данных : [length<8bit>][elem<elem_type>]*length

        :param elem_type: Тип данных, поддерживаемый методом read
        :type elem_type: type
        :param lazy: Факт ленивости
        :type lazy: bool
        :param extra_kwargs: kwargs для метода 'read' загружаемого типа
        :type extra_kwargs: dict
        :return: Последовательность однотипных данных
        :rtype: list или generator
        """
        length = self.read_byte()
        if lazy:
            for elem in self.__read_iterable(length, elem_type, True, extra_kwargs):
                yield elem
        else:
            return self.__read_iterable(length, elem_type, False, extra_kwargs)
