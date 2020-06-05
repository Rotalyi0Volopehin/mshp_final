import exceptions

from game_eng.player import Player
from game_eng.grid_tile import GridTile
# vvv импорты для чтения/записи vvv
from net_connection.core_classes import CoreClasses
from io_tools.binary_reader import BinaryReader
from io_tools.binary_writer import BinaryWriter


class PlayerAction:
    """**Модель действия, совершаемого игроком**\n
    abstract class\n
    Этот класс необходим для журналирования ходов.
    """
    def __init__(self, player: Player, target: GridTile):
        if not isinstance(player, Player):
            raise exceptions.ArgumentTypeException()
        self.player = player
        self.target = target

    @staticmethod
    def _read_tile(stream, tiles):
        loc_x, loc_y = stream.read_byte_point()
        return tiles[loc_x][loc_y]

    @staticmethod
    def read(stream: BinaryReader, game_model):
        if not isinstance(stream, BinaryReader):
            raise exceptions.ArgumentTypeException()
        action_type = CoreClasses.read_class(stream)
        uid = stream.read_uint()
        player = game_model.player_ids[uid]
        target = PlayerAction._read_tile(stream, game_model.grid.tiles)
        obj = action_type(player, target)
        if hasattr(action_type, "read_ext"):
            action_type.read_ext(stream, obj, game_model)
        return obj

    @staticmethod
    def write(stream: BinaryWriter, obj):
        if not (isinstance(stream, BinaryWriter) and isinstance(obj, PlayerAction)):
            raise exceptions.ArgumentTypeException()
        CoreClasses.write_class(stream, type(obj))
        stream.write_uint(obj.player.id)
        target_loc = (obj.target.loc_x, obj.target.loc_y)
        stream.write_byte_point(target_loc)
        if hasattr(type(obj), "write_ext"):
            type(obj).write_ext(stream, obj)

    def try_do(self) -> bool:
        """**Попытка совершить действие**\n
        :raises NotImplementedException: |NotImplementedException|
        :return: ok
        :rtype: bool
        """
        raise exceptions.NotImplementedException()

    def try_undo(self) -> bool:
        """**Попытка отменить действие**\n
        :raises NotImplementedException: |NotImplementedException|
        :return: ok
        :rtype: bool
        """
        raise exceptions.NotImplementedException()
