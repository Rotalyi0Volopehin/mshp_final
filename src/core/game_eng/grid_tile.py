import exceptions

# vvv импорты для чтения/записи vvv
from net_connection.core_classes import CoreClasses
from io_tools.binary_reader import BinaryReader
from io_tools.binary_writer import BinaryWriter


class GridTile:
    def __init__(self, grid, loc_x, loc_y, team=None):
        self.grid = grid
        self.power = 2
        self.loc_x = loc_x
        self.loc_y = loc_y
        self.team_ind = -1
        self.team = team
        self.controller = self.view = None
        self.effects = set()

    @staticmethod
    def read(stream: BinaryReader, grid):
        if not isinstance(stream, BinaryReader):
            raise exceptions.ArgumentTypeException()
        tile_type = CoreClasses.read_class(stream)
        loc_x, loc_y = stream.read_byte_point()
        team_ind = stream.read_sbyte()
        obj = tile_type(grid, loc_x, loc_y)
        obj.team_ind = team_ind
        power = stream.read_byte()
        obj.gain_power(power)
        for effect in stream.read_short_iterable(GridTile.get_effect_type(), {"tile": obj}):
            obj.add_effect(effect)
        return obj

    @staticmethod
    def write(stream: BinaryWriter, obj):
        if not (isinstance(stream, BinaryWriter) and isinstance(obj, GridTile)):
            raise exceptions.ArgumentTypeException()
        CoreClasses.write_class(stream, type(obj))
        stream.write_byte_point((obj.loc_x, obj.loc_y))
        stream.write_sbyte(obj.team_ind)
        stream.write_byte(obj.power)
        stream.write_short_iterable(obj.effects, GridTile.get_effect_type())

    @staticmethod  # костыль для избежания циклического импорта
    def get_effect_type() -> type:
        if not hasattr(GridTile, "__effect_type"):
            from game_eng.grid_tile_effect import GridTileEffect
            GridTile.__effect_type = GridTileEffect
        return GridTile.__effect_type

    def add_effect(self, effect):
        if not isinstance(effect, GridTile.get_effect_type()):
            raise exceptions.ArgumentTypeException()
        # vvv необходимо, чтобы на одной клетке было не долее одного эффекта одного типа
        self.__remove_effect_with_type(type(effect))
        self.effects.add(effect)

    def __remove_effect_with_type(self, effect_type: type):
        for effect in self.effects:
            if type(effect) == effect_type:
                self.effects.remove(effect)
                break

    def remove_effect(self, effect):
        if not isinstance(effect, GridTile.get_effect_type()):
            raise exceptions.ArgumentTypeException()
        if effect in self.effects:
            self.effects.remove(effect)

    def has_effect(self, effect_type: type) -> bool:
        if not isinstance(effect_type, type):
            raise exceptions.ArgumentTypeException()
        if not issubclass(effect_type, GridTile.get_effect_type()):
            raise exceptions.ArgumentValueException()
        for effect in self.effects:
            if type(effect) == effect_type:
                return True
        return False

    def clear_effects(self):
        self.effects.clear()

    @property
    def team(self):
        return None if self.team_ind < 0 else self.grid.game.teams[self.team_ind]

    @team.setter
    def team(self, value):
        self.team_ind = -1 if value is None else value.index

    @property
    def even_row(self) -> bool:
        return (self.loc_y & 1) == 0

    @property
    def odd_row(self) -> bool:
        return (self.loc_y & 1) == 1

    def set_view(self, view):
        self.view = view

    def set_controller(self, controller):
        self.controller = controller

    def get_neighbours(self) -> set:
        neighbours = set()

        def try_add_neighbour(dx, dy):
            neighbour_x = self.loc_x + dx
            neighbour_y = self.loc_y + dy
            if (neighbour_x >= 0) and (neighbour_x < self.grid.width) and\
                    (neighbour_y >= 0) and (neighbour_y < self.grid.height):
                neighbour = self.grid.tiles[neighbour_x][neighbour_y]
                if neighbour is not None:
                    neighbours.add(neighbour)
        try_add_neighbour(-1, 0)
        try_add_neighbour(1, 0)
        try_add_neighbour(0, -1)
        try_add_neighbour(0, 1)
        shift = 1 if self.odd_row else -1
        try_add_neighbour(shift, -1)
        try_add_neighbour(shift, 1)
        return neighbours

    def conquer(self, team):
        self.team = team
        self.power = abs(self.power)

    def try_move_power_as_team(self, target, value: int, team, cut_surplus: bool = False) -> bool:
        if (self.team != team) or ((target.team is None) and (value < 0)):
            return False
        self.move_power(target, value, cut_surplus)
        return True

    def move_power(self, target, value: int, cut_surplus: bool = False):
        if not (isinstance(target, GridTile) and isinstance(value, int) and isinstance(cut_surplus, bool)):
            raise exceptions.ArgumentTypeException()
        value = self.__check_and_correct_value_for_power_movement(value, cut_surplus)
        if self.team == target.team:
            value = -target.__check_and_correct_value_for_power_movement(-value, cut_surplus)
            self.__ally_power_movement(target, value)
        else:
            value = target.__check_and_correct_value_for_power_movement(value, cut_surplus, True)
            self.__foe_power_movement(target, value)

    def __check_and_correct_value_for_power_movement(self, value: int, cut_surplus: bool, foe: bool = False) -> int:
        if not foe and (self.power < value):
            if cut_surplus:
                return self.power
            else:
                raise exceptions.ArgumentOutOfRangeException()
        elif self.power - self.power_cap > value:
            if cut_surplus:
                return self.power - self.power_cap
            else:
                raise exceptions.ArgumentOutOfRangeException()
        return value

    def __ally_power_movement(self, target, value):
        self.power -= value
        target.power += value

    def __foe_power_movement(self, target, value):
        self.power -= value
        target.power -= value
        if target.power < 0:
            target.conquer(self.team)

    def handle_new_team_turn(self):
        if self.grid.game.current_team == self.team:
            income = self.owners_income
            power_growth = self.power_growth
            if not (isinstance(income, int) and isinstance(power_growth, int)):
                raise exceptions.InvalidReturnException()
            self.team.earn_money(income)
            self.gain_power(power_growth)
        for effect in set(self.effects):
            effect.apply()

    @property  # virtual
    def owners_income(self) -> int:
        return 0

    @property  # virtual
    def power_growth(self) -> int:
        return 1

    @property  # virtual
    def power_cap(self) -> int:
        return 64

    @property  # virtual
    def name(self) -> str:
        return "Обыкновенный Кластер"

    @staticmethod
    def get_upgrade_price() -> int:
        return 0

    def upgrade(self, tile_type: type):
        if not isinstance(tile_type, type):
            raise exceptions.ArgumentTypeException()
        if not issubclass(tile_type, GridTile):
            raise exceptions.ArgumentValueException()
        new_tile = tile_type(self.grid, self.loc_x, self.loc_y, self.team)
        new_tile.gain_power(self.power)
        self.grid.tiles[self.loc_x][self.loc_y] = new_tile
        return new_tile

    def take_damage(self, value):
        self.power = max(self.power - value, 0)

    def gain_power(self, value):
        self.power = min(self.power + value, self.power_cap)
