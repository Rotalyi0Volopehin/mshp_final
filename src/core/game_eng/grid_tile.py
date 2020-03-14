import exceptions


# TODO: задокументировать


class GridTile:
    def __init__(self, grid, loc_x: int, loc_y: int):
        # vvv проверка параметров vvv
        if not (isinstance(loc_x, int) and isinstance(loc_y, int)):
            raise exceptions.ArgumentTypeException()
        if not grid.is_point_in_bounds(loc_x, loc_y):
            raise exceptions.ArgumentValueException("Location is out of bounds!")
        # vvv инициализация vvv
        self.grid = grid
        self.__loc_x = loc_x
        self.__loc_y = loc_y

    @property
    def loc_x(self):
        return self.__loc_x

    @property
    def loc_y(self):
        return self.__loc_y

    def get_neighbours(self):
        return self.grid.get_tile_neighbours(self)
