import exceptions

from datetime import datetime
from struct import unpack
from .binary_stream import BinaryStream


class BinaryReader(BinaryStream):
    def __init__(self, base_stream=None, data=None):
        super().__init__(base_stream, data)
        self.__read_methods = {
            int: self.read_int,
            bool: self.read_bool,
            str: self.read_string,
        }

    @staticmethod
    def get_stream_of_file(file_path: str):
        """**Получение потока файла**\n
        :param file_path: Путь до файла, поток которого требуется получить
        :type file_path: str
        :return: Поток
        :rtype: BinaryReader
        """
        file = open(file_path, "br")
        stream = BinaryReader(data=file.read())
        file.close()
        return stream

    def read_int(self) -> int:
        """**Чтение Int32**\n
        Формат данных : [data<32bit>]

        :return: Int32
        :rtype: int
        """
        bin_ = self.base_stream.read(4)
        return unpack('>i', bin_)[0]

    def read_uint(self) -> int:
        """**Чтение UnsignedInt32**\n
        Формат данных : [data<32bit>]

        :return: UnsignedInt32
        :rtype: int
        """
        bin_ = self.base_stream.read(4)
        return unpack('>I', bin_)[0]

    def read_byte(self) -> int:
        """**Чтение UnsignedInt8**\n
        Формат данных : [data<8bit>]

        :return: UnsignedInt8
        :rtype: int
        """
        bin_ = self.base_stream.read(1)
        return unpack('B', bin_)[0]

    def read_sbyte(self) -> int:
        """**Чтение Int8**\n
        Формат данных : [data<8bit>]

        :return: Int8
        :rtype: int
        """
        bin_ = self.base_stream.read(1)
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

    def read_datetime(self):
        """**Чтение DateTime**\n
        Формат данных : [int_part<32bit>][float_part<32bit>]

        :return: DateTime
        :rtype: datetime
        """
        int_part = self.read_uint()
        float_part = self.read_uint()
        timestamp = int_part + float_part / 1000000
        return datetime.fromtimestamp(timestamp)

    def read_chars(self, length: int) -> str:
        """**Чтение строки известной длины**\n
        Формат данных : [chars<bytes>]

        :param length: Длина строки
        :type length: int
        :return: Строка
        :rtype: str
        """
        bin_ = self.base_stream.read(length)
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

    def __read_iterable(self, length: int, elem_type: type, extra_kwargs: dict):
        read_method = self.__get_read_method(elem_type, extra_kwargs)
        data = length * [None]
        for i in range(length):
            data[i] = read_method()
        return data

    def read_iterable(self, elem_type: type, extra_kwargs: dict = None):
        """**Чтение последовательности однотипных данных**\n
        Формат данных : [length<32bit>][elem<elem_type>]*length

        :param elem_type: Тип данных, поддерживаемый методом read
        :type elem_type: type
        :param extra_kwargs: kwargs для метода 'read' загружаемого типа
        :type extra_kwargs: dict
        :return: Последовательность однотипных данных
        :rtype: list
        """
        length = self.read_uint()
        return self.__read_iterable(length, elem_type, extra_kwargs)

    def read_short_iterable(self, elem_type: type, extra_kwargs: dict = None):
        """**Чтение последовательности однотипных данных длиной до 255 элементов**\n
        Формат данных : [length<8bit>][elem<elem_type>]*length

        :param elem_type: Тип данных, поддерживаемый методом read
        :type elem_type: type
        :param extra_kwargs: kwargs для метода 'read' загружаемого типа
        :type extra_kwargs: dict
        :return: Последовательность однотипных данных
        :rtype: list
        """
        length = self.read_byte()
        return self.__read_iterable(length, elem_type, extra_kwargs)
