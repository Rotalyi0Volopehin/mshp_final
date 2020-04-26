from random import randint
import pygame
import math
from constants import Color
from objects.base import DrawObject
from objects.text import Text
import time


class GridTile(DrawObject):
    # Возможные состояния игровой клетки:
    #   black - наша невидимая черная стена
    #   white - не выбрана
    #   red - выбрана
    #   green - соседняя с выбранной
    #   orange - та клетка, куда двигаем все, что хотим

    def __init__(self, game, side, color, even, screen_x, screen_y, wall, x, y):
        super().__init__(game)
        self.even = even  # чет нечет строчка
        self.start_value = randint(0, 60)  # ранд количество юнитов
        self.value = self.start_value
        self.x = x  # координаты смещений
        self.y = y
        self.pos_x = screen_x  # на экране позиция
        self.pos_y = screen_y
        self.team_color = color
        self.color = color
        self.side = side
        self.sq = 3 ** (1 / 2)
        self.hex_points = [(self.side / 2, 0),
                           (1.5 * self.side, 0),
                           (2 * self.side, self.sq * self.side / 2),
                           (1.5 * self.side, self.sq * self.side),
                           (self.side / 2, self.sq * self.side),
                           (0, self.sq * self.side / 2)]
        self.number = Text(game=self.game, text=str(self.value), font_size=20, x=self.pos_x + self.side,
                           y=self.pos_y + self.sq * self.side / 2)
        self.invisible_wall = wall
        self.surface = pygame.Surface((2 * self.side, 2 * self.side))
        self.update_surface()

    def update_surface(self):
        self.surface = pygame.Surface((2 * self.side, 2 * self.side))
        self.surface.set_colorkey(Color.BLACK)
        #self.number.update_text(str(self.x)+" "+str(self.y))
        self.number.update_text(str(self.value))
        pygame.draw.polygon(self.surface, self.color, self.hex_points, 5)

    def process_draw(self):
        self.update_surface()
        if not(self.invisible_wall):
            self.number.process_draw()
        self.game.screen.blit(self.surface, (self.pos_x, self.pos_y))

    def get_neighbours(self):  # HEчет-q
        top_x = self.x
        top_y = self.y - 1

        bot_x = self.x
        bot_y = self.y + 1

        left_top_x = self.x - 1
        left_top_y = self.y - 1

        right_top_x = self.x - 1
        right_top_y = self.y + 1

        right_bot_x = self.x+1
        right_bot_y = self.y

        left_bot_x = self.x -1
        left_bot_y = self.y

        if not (self.even):
            left_top_x = self.x - 1
            left_top_y = self.y

            right_top_x = self.x + 1
            right_top_y = self.y

            left_bot_x = self.x +1
            right_bot_y = self.y -1

            right_bot_x = self.x + 1
            left_bot_y = self.y +1

        # создадим список а, с коордами всех клеток. Обход с верхней клетки против часовой стрелки
        a = [[top_x, top_y], [right_top_x, right_top_y], [right_bot_x, right_bot_y], [bot_x, bot_y],
             [left_bot_x, left_bot_y], [left_top_x, left_top_y]]
        return a

    def set_color_to_team(self):
        self.color = self.team_color

    def set_team_color(self, color):
        self.team_color = color

    def set_color(self, color):
        self.color = color
        self.update_surface()

    def return_color(self):
        return self.color

    def set_wall(self):
        self.invisible_black_wall = True
        self.color = Color.BLACK


# noinspection PyRedundantParentheses
class GridModel(DrawObject):
    def __init__(self, game, hex_side=20, width=14, height=5, delta=4):
        super().__init__(game)
        self.sq = 3 ** (1 / 2)
        self.extra = hex_side / 2 - delta * self.sq
        self.hex_draw_array = [
            [0] * (height) for i in range(width)
        ]
        self.height = height
        self.width = width
        self.delta = delta
        self.team_colors = [Color.BLUE, (255,50,255), (50,255,255), (255,255,50)]
        i = -1  # x,y смещений
        j = 0
        for column in range(self.height):  # нечет-q https://habr.com/ru/post/319644/
            i += 2
            j = 0
            for row in range(self.width):
                j += 1
                self.add_cell(game, hex_side, Color.WHITE, row, column, False, i, j)
        self.set_cell_color_x_y(0,0,Color.BLUE, Color.BLUE)
        print(i,j)
        self.hex_draw_array[self.width-1][self.height-1].set_team_color((255,50,255))
        self.hex_draw_array[0][self.height - 1].set_team_color((255,255,50))
        self.hex_draw_array[self.width - 1][0].set_team_color((50,255,255))




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

    def set_cell_color_x_y(self, x, y, color, team_color=False):
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
            if redcell.value-value >= 0 and orangecell.value+value>=0:
                redcell.value -= value
                orangecell.value += value
        elif value>0:
            self.attack_cell_units(redcell,orangecell,value)

    def attack_cell_units(self, redcell, orangecell, value):
        if redcell.value-value >= 0 and orangecell.value-value>=0:
            redcell.value -= value
            orangecell.value -= value
        if orangecell.value <= 0:
            orangecell.set_team_color(redcell.team_color)
            orangecell.value = orangecell.start_value # соответствия с нашей механикой

    def ability_emp(self,cell):
        neighbours = cell.get_neighbours()
        for row in range(6):
            cell = self.get_cell_by_x_y(neighbours[row][0], neighbours[row][1])
            if cell:
                cell.value -= 20
                if cell.value <0:
                    cell.value = 0
                    #TODO: self.get_cell_by_x_y(neighbours[row][0], neighbours[row][1]).set_team_color =

    def ability_fishing(self,cell):
        cell.value -= 20
        if cell.value <0:
            cell.value = 0
            #TODO: cell.set_team_color =
            # cell.value = cell.start_value