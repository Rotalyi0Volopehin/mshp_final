import exceptions

from game_eng.grid_tile import GridTile
# vvv импорты для чтения/записи vvv
from net_connection.core_classes import CoreClasses
from io_tools.binary_reader import BinaryReader
from io_tools.binary_writer import BinaryWriter


class GridTileEffect:
    def __init__(self, tile: GridTile):
        if not isinstance(tile, GridTile):
            raise exceptions.ArgumentTypeException()
        tile.add_effect(self)
        self.tile = tile

    @staticmethod
    def read(stream: BinaryReader, tile: GridTile):
        if not (isinstance(stream, BinaryReader) and isinstance(tile, GridTile)):
            raise exceptions.ArgumentTypeException()
        effect_type = CoreClasses.read_class(stream)
        obj = effect_type(tile)
        return obj

    @staticmethod
    def write(stream: BinaryWriter, obj):
        if not (isinstance(stream, BinaryWriter) and isinstance(obj, GridTileEffect)):
            raise exceptions.ArgumentTypeException()
        CoreClasses.write_class(stream, type(obj))

    @property  # abstract
    def name(self) -> str:
        raise exceptions.NotImplementedException()

    # abstract
    def apply(self):
        pass
