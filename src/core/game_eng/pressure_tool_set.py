import exceptions

from game_eng.grid_tile import GridTile
from game_eng.player import Player
# vvv импорты для чтения/записи vvv
from net_connection.core_classes import CoreClasses
from io_tools.binary_reader import BinaryReader
from io_tools.binary_writer import BinaryWriter


class PressureToolSet:
    """**Множество ИВ одного типа**\n
    abstract class\n
    Все наследующие классы должны располагаться в директории 'pressure_tool_set_ders'.
    """
    def __init__(self, player: Player = None):
        if not (isinstance(player, Player) or (player is None)):
            raise exceptions.ArgumentTypeException()
        self._player = player
        if player is None:  # в магазине
            self.count = self.start_market_count
            if not isinstance(self.count, int):
                raise exceptions.InvalidReturnException()
        else:  # у игрока
            self.count = 0

    @staticmethod
    def read(stream: BinaryReader, player: Player = None):
        if not (isinstance(stream, BinaryReader) and (isinstance(player, Player) or (player is None))):
            raise exceptions.ArgumentTypeException()
        pts_type = CoreClasses.read_class(stream)
        count = stream.read_uint()
        obj = pts_type(player)
        obj.count = count
        return obj

    @staticmethod
    def write(stream: BinaryWriter, obj):
        if not (isinstance(stream, BinaryWriter) and isinstance(obj, PressureToolSet)):
            raise exceptions.ArgumentTypeException()
        CoreClasses.write_class(stream, type(obj))
        stream.write_uint(obj.count)

    @property
    def start_market_count(self) -> int:
        """**Количество ИВ этого типа в Даркнете в начале игры**\n
        abstract property

        :raises NotImplementedException: |NotImplementedException|
        :return: Количество ИВ
        :rtype: int
        """
        raise exceptions.NotImplementedException()

    @property
    def production_cost(self) -> int:
        """**Стоимость изготовления одного ИВ этого типа**\n
        abstract property

        :raises NotImplementedException: |NotImplementedException|
        :return: Стоимость изготовления
        :rtype: int
        """
        raise exceptions.NotImplementedException()

    @property
    def name(self) -> str:
        """**Название ИВ этого типа**\n
        abstract property

        :raises NotImplementedException: |NotImplementedException|
        :return: Название ИВ
        :rtype: str
        """
        raise exceptions.NotImplementedException()

    def try_use(self, target: GridTile) -> bool:
        """**Попытка использования одного ИВ этого типа**\n
        Пробует использовать один ИВ этого типа на указанной клетке поля.
        Уменьшает количество ИВ в множестве на один, если удачно.

        :raises ArgumentTypeException: |ArgumentTypeException|
        :raises InvalidReturnException: |InvalidReturnException|
        :param target: Клетка поля, на которой применяется ИВ
        :type target: GridTile
        :return: ok
        :rtype: bool
        """
        if not isinstance(target, GridTile):
            raise exceptions.ArgumentTypeException()
        if self.count <= 0:
            return False
        ok = self._try_apply(target)
        if not isinstance(ok, bool):
            raise exceptions.InvalidReturnException()
        if ok:
            self.count -= 1
        return ok

    def try_cancel(self) -> bool:
        raise exceptions.NotImplementedException()

    def _try_apply(self, target: GridTile) -> bool:
        """**Попытка применения эффекта ИВ этого типа**\n
        abstract method\n
        Применяет эффект ИВ этого типа на указанной клетке поля.

        :raises NotImplementedException: |NotImplementedException|
        :param target: Клетка поля, на которой применяется эффект ИВ
        :type target: GridTile
        :return: ok
        :rtype: bool
        """
        raise exceptions.NotImplementedException()
