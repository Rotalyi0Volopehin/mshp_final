import math

from constants import Color
from game_eng.grid_tile import GridTile


# TODO: Андрей, это не модель!!
# В этом классе не должно быть цветов!


# noinspection PyRedundantParentheses
class GridModel:
    def __init__(self, game, hex_side=20, width=14, height=5, delta=4):
        super().__init__(game)
        self.sq = 3 ** 0.5
        self.extra = hex_side / 2 - delta * self.sq
        self.hex_draw_array = [
            [0] * (height) for i in range(width)
        ]
        self.height = height
        self.width = width
        self.delta = delta
        i = -1  # x, y смещений
        for column in range(self.height):  # нечет-q https://habr.com/ru/post/319644/
            i += 2
            j = 0
            for row in range(self.width):
                j += 1
                self.add_cell(game, hex_side, Color.WHITE, row, column, False, i, j)
        self.set_cell_color_x_y(4, 4, Color.BLUE, Color.BLUE)

    def add_cell(self, game, hex_side, color, row, column, is_wall, x, y):
        self.hex_draw_array[row][column] = GridTile(
            game,
            hex_side,
            color,
            True if row % 2 == 0 else False,
            column * (hex_side * 4 - 2 * self.extra) if row % 2 == 0 else 2 * hex_side + (4 * hex_side) * column - (
                        2 * (column + 1) - 1) * self.extra,
            row * (self.sq * hex_side / 2 + self.delta) if row % 2 == 0 else self.sq * hex_side / 2 + (row - 1) * (
                        self.sq * hex_side / 2 + self.delta) + self.delta,
            is_wall,
            math.floor(y / 2) if row % 2 == 0 else math.floor(y / 2 - 1),
            x - 1 if row % 2 == 0 else x,
        )

    def inPolygon(self, x, y):
        for row in range(self.width):
            for column in range(self.height):
                cell = self.hex_draw_array[row][column]
                if (y >= cell.pos_y) and (y <= cell.pos_y + cell.sq * cell.side) \
                        and (x >= cell.pos_x) and (x <= cell.pos_x + 1.5 * cell.side):
                    return cell

    def get_cell_by_x_y(self, x, y):
        for row in range(self.width):
            for column in range(self.height):
                if self.hex_draw_array[row][column].x == x and self.hex_draw_array[row][column].y == y:
                    return self.hex_draw_array[row][column]
        return None

    def get_cell_by_colour(self, color):
        for row in range(self.width):
            for column in range(self.height):
                cell = self.hex_draw_array[row][column]
                if (cell.return_color() == color):
                    return cell
        return None

    def set_all_team_color(self):
        for row in range(self.width):
            for column in range(self.height):
                self.hex_draw_array[row][column].set_color_to_team()

    def set_cell_color_x_y(self, x, y, color, team_color=None):
        cell = self.get_cell_by_x_y(x, y)
        if not cell:
            return
        cell.set_color(color)
        if team_color:
            cell.set_team_color(team_color)

    def get_cell_color(self, row, column):
        return self.hex_draw_array[row][column].return_color()

    def make_cell_green(self, cell):
        if cell:
            cell.set_color(Color.GREEN)

    def make_cells_green(self, cell):
        neighbours = cell.get_neighbours()
        for row in range(6):
            if self.get_cell_by_x_y(neighbours[row][0], neighbours[row][1]):
                self.make_cell_green(self.get_cell_by_x_y(neighbours[row][0], neighbours[row][1]))

    def move_units(self, redcell, orangecell, value):
        if not redcell:
            return
        if not orangecell:
            return
        if orangecell.team_color == redcell.team_color:
            if redcell.value - value >= 0 and orangecell.value + value >= 0:
                redcell.value -= value
                orangecell.value += value
        elif value > 0:
            self.attack_cell_units(redcell, orangecell, value)

    def attack_cell_units(self, redcell, orangecell, value):
        if redcell.value-value >= 0 and orangecell.value-value >= 0:
            redcell.value -= value
            orangecell.value -= value
        if orangecell.value <= 0:
            orangecell.set_team_color(redcell.team_color)
            orangecell.value = orangecell.start_value  # соответствия с нашей механикой

    # TODO: вынести абилки в отдельные классы

    def ability_emp(self, cell):
        neighbours = cell.get_neighbours()
        for row in range(6):
            cell = self.get_cell_by_x_y(neighbours[row][0], neighbours[row][1])
            if cell:
                cell.value -= 20
                if cell.value < 0:
                    cell.value = 0
                    #TODO: self.get_cell_by_x_y(neighbours[row][0], neighbours[row][1]).set_team_color =

    def ability_fishing(self, cell):
        cell.value -= 20
        if cell.value < 0:
            cell.value = 0
            #TODO: cell.set_team_color =
            # cell.value = cell.start_value