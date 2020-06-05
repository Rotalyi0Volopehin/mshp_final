import exceptions

from game_eng.grid_tile import GridTile
# vvv импорты для чтения/записи vvv
from io_tools.binary_reader import BinaryReader
from io_tools.binary_writer import BinaryWriter


class GridModel:
    def __init__(self, game, width: int, height: int):
        if not (isinstance(width, int) and isinstance(height, int)):
            raise exceptions.ArgumentTypeException()
        self.game = game
        self.height = height
        self.width = width
        self.tiles = None
        self.__create_tiles()
        self.controller = self.view = None

    @staticmethod
    def read(stream: BinaryReader, game_model):
        if not isinstance(stream, BinaryReader):
            raise exceptions.ArgumentTypeException()
        width = stream.read_byte()
        height = stream.read_byte()
        obj = GridModel(game_model, width, height)
        for ix, iy in obj.foreach_loc:
            obj.tiles[ix][iy] = GridTile.read(stream, obj)
        return obj

    @staticmethod
    def write(stream: BinaryWriter, obj):
        if not (isinstance(stream, BinaryWriter) and isinstance(obj, GridModel)):
            raise exceptions.ArgumentTypeException()
        stream.write_byte(obj.width)
        stream.write_byte(obj.height)
        for ix, iy in obj.foreach_loc:
            GridTile.write(stream, obj.tiles[ix][iy])

    @property
    def foreach(self):
        for ix in range(self.width):
            for iy in range(self.height):
                tile = self.tiles[ix][iy]
                if tile is not None:
                    yield tile

    @property
    def foreach_loc(self):
        for ix in range(self.width):
            for iy in range(self.height):
                yield ix, iy

    def __create_tiles(self):
        self.tiles = []
        for ix in range(self.width):
            column = []
            for iy in range(self.height):
                tile = GridTile(self, ix, iy)
                column.append(tile)
            self.tiles.append(column)

    def set_view(self, view):
        self.view = view

    def set_controller(self, controller):
        self.controller = controller

    def handle_new_team_turn(self):
        for tile in self.foreach:
            tile.handle_new_team_turn()
