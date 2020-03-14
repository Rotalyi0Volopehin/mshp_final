import exceptions

from game_eng.grid_tile import GridTile


# TODO: задокументировать


# хексагональная сетка для карты; поле tiles содержит клетки (None -- дыра)
class Grid:
    def __init__(self, width: int, height: int):
        # vvv проверка параметров vvv
        if not (isinstance(width, int) and isinstance(height, int)):
            raise exceptions.ArgumentTypeException()
        if (width < 1) or (height < 1):
            raise exceptions.ArgumentValueException()
        # vvv инициализация vvv
        self.__width = width
        self.__height = height
        self._tiles = [None] * width
        for ix in range(width):
            self._tiles[ix] = [GridTile(self, ix, iy) for iy in range(height)]

    @property
    def width(self) -> int:
        return self.__width

    @property
    def height(self) -> int:
        return self.__height

    @property
    def size(self) -> ():
        return self.__width, self.__height

    def is_point_in_bounds(self, loc_x: int, loc_y: int) -> bool:
        if (loc_x < 0) or (loc_y < 0):
            return False
        return (loc_x < self.__width) and (loc_y < self.__height)

    def does_tile_exist_on(self, loc_x: int, loc_y: int) -> bool:
        if self.is_point_in_bounds(loc_x, loc_y):
            return False
        return self._tiles[loc_x][loc_y] is not None

    def get_tile_neighbours(self, tile: GridTile) -> [GridTile]:
        neighbours = []

        def try_add_tile_neighbour(loc_x: int, loc_y: int):
            if self.does_tile_exist_on(loc_x, loc_y):
                neighbours.append(self._tiles[loc_x][loc_y])
        try_add_tile_neighbour(tile.__loc_x - 1, tile.__loc_y)
        try_add_tile_neighbour(tile.__loc_x + 1, tile.__loc_y)
        try_add_tile_neighbour(tile.__loc_x, tile.__loc_y - 1)
        try_add_tile_neighbour(tile.__loc_x, tile.__loc_y + 1)
        x = tile.__loc_x - 1 if (tile.__loc_y & 1) == 0 else tile.__loc_x + 1
        try_add_tile_neighbour(x, tile.__loc_y - 1)
        try_add_tile_neighbour(x, tile.__loc_y + 1)
