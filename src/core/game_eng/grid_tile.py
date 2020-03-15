import exceptions

from game_eng.game_object_model import GameObjectModel


# TODO: задокументировать


class GridTile(GameObjectModel):
    def __init__(self, grid, loc_x: int, loc_y: int, team: int = -1):
        # vvv проверка параметров vvv
        if not (isinstance(loc_x, int) and isinstance(loc_y, int) and isinstance(team, int)):
            raise exceptions.ArgumentTypeException()
        if not grid.is_point_in_bounds(loc_x, loc_y):
            raise exceptions.ArgumentValueException("Location is out of bounds!")
        if (team < -1) or (team > 2):
            raise exceptions.ArgumentValueException()
        # vvv инициализация vvv
        self.team = team  # может принимать значения от -1 до 2 (-1 -- нейтральная клетка)
        self.__loc_x = loc_x
        self.__loc_y = loc_y

    @property
    def loc_x(self):
        return self.__loc_x

    @property
    def loc_y(self):
        return self.__loc_y

    def get_neighbours(self, grid):
        return grid.get_tile_neighbours(self)
