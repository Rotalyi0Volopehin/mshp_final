import exceptions

from random import randint


class GridTile:
    def __init__(self, grid, loc_x, loc_y, team=None):
        self.grid = grid
        self.power = randint(0, 60)  # ранд количество юнитов
        self.loc_x = loc_x
        self.loc_y = loc_y
        self.team = team
        self.controller = self.view = None

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

    def handle_new_turn(self):
        if self.grid.game.current_team == self.team:
            income = self.owners_income
            power_growth = self.power_growth
            if not (isinstance(income, int) and isinstance(power_growth, int)):
                raise exceptions.InvalidReturnException()
            self.team.earn_money(income)
            self.gain_power(power_growth)

    @property  # virtual
    def owners_income(self) -> int:
        return 0

    @property  # virtual
    def power_growth(self) -> int:
        return 1

    @property  # virtual
    def power_cap(self) -> int:
        return 64

    def take_damage(self, value):
        self.power = max(self.power - value, 0)

    def gain_power(self, value):
        self.power = min(self.power + value, self.power_cap)
