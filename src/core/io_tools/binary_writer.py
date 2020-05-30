import exceptions

from struct import pack
from .binary_stream import BinaryStream


class BinaryWriter(BinaryStream):
    def __init__(self, base_stream, data):
        super().__init__(base_stream, data)
        self.__write_methods = {
            int: self.write_int,
            bool: self.write_byte,
            str: self.write_string,
        }

    def write_int(self, data: int):
        """**Запись Int32**\n
        Формат данных : [data<32bit>]

        :param data: Int32
        :type data: int
        """
        bin_ = pack('>I', data)
        self.__base_stream.write(bin_)

    def write_uint(self, data: int):
        """**Запись UnsignedInt32**\n
        Формат данных : [data<32bit>]

        :param data: UnsignedInt32
        :type data: int
        """
        bin_ = pack('>I', data)
        self.__base_stream.write(bin_)

    def write_byte(self, data: int):
        """**Запись UnsignedInt8**\n
        Формат данных : [data<8bit>]

        :param data: UnsignedInt8
        :type data: int
        """
        bin_ = pack('B', data)
        self.__base_stream.write(bin_)

    def write_sbyte(self, data: int):
        """**Запись Int8**\n
        Формат данных : [data<8bit>]

        :param data: Int8
        :type data: int
        """
        bin_ = pack('b', data)
        self.__base_stream.write(bin_)

    def write_bool(self, data: bool):
        """**Запись Boolean**\n
        Формат данных : [data<8bit>]

        :param data: Boolean
        :type data: bool
        """
        self.write_byte(data)

    def write_int_point(self, data: tuple):
        """**Запись точки Int32**\n
        Формат данных : [x<32bit>][y<32bit>]

        :param data: Точка Int32
        :type data: (int, int)
        """
        self.write_int(data[0])
        self.write_int(data[1])

    def write_uint_point(self, data: tuple):
        """**Запись точки UnsignedInt32**\n
        Формат данных : [x<32bit>][y<32bit>]

        :param data: Точка UnsignedInt32
        :type data: (int, int)
        """
        self.write_uint(data[0])
        self.write_uint(data[1])

    def write_byte_point(self, data: tuple):
        """**Запись точки UnsignedInt8**\n
        Формат данных : [x<8bit>][y<8bit>]

        :param data: Точка UnsignedInt8
        :type data: (int, int)
        """
        self.write_byte(data[0])
        self.write_byte(data[1])

    def write_sbyte_point(self, data: tuple):
        """**Запись точки Int8**\n
        Формат данных : [x<8bit>][y<8bit>]

        :param data: Точка Int8
        :type data: (int, int)
        """
        self.write_sbyte(data[0])
        self.write_sbyte(data[1])

    def write_chars(self, data: str):
        """**Запись строки известной длины**\n
        Формат данных : [chars<bytes>]

        :param data: Строка
        :type data: str
        """
        bin_ = data.encode()
        self.__base_stream.write(bin_)

    def write_string(self, data: str):
        """**Запись строки**\n
        Формат данных : [length<32bit>][chars<bytes>]

        :param data: Строка
        :type data: str
        """
        self.write_uint(len(data))
        self.write_chars(data)

    def write_short_string(self, data: str):
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
        self.write_uint(len(iterable))
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
