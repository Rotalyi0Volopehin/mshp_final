from random import randint

import pygame

from constants import Color
from objects.base import DrawObject
from objects.text import Text


class GridTile(DrawObject):
    # Возможные состояния игровой клетки:
    #   black - наша невидимая черная стена
    #   white - не выбрана
    #   red - выбрана
    #   green - соседняя с выбранной
    #   orange - та клетка, куда двигаем ОЧКИ ЮНИТЫ ВИРУСЫ БОТНЕТЫ ФАЙРВОЛЛЫ и тд.

    def __init__(self, game, x, y, side, number_units, even, pos_x, pos_y, wall, color):
        super().__init__(game)
        self.even = even  # чет нечет строчка
        self.nx = number_units  # ранд количество юнитов
        self.x = x #координаты смещений
        self.y = y

        self.pos_x = pos_x #на экране позиция
        self.pos_y = pos_y
        self.color = color
        self.side = side
        self.sq = 3 ** (1 / 2)
        self.hex_points = [(self.side / 2, 0),
                           (1.5 * self.side, 0),
                           (2 * self.side, self.sq * self.side / 2),
                           (1.5 * self.side, self.sq * self.side),
                           (self.side / 2, self.sq * self.side),
                           (0, self.sq * self.side / 2)]

        self.surface = pygame.Surface((2 * self.side, 2 * self.side))
        self.surface.set_colorkey(Color.BLACK)
        pygame.draw.polygon(self.surface, self.color, self.hex_points, 5)
        self.number = Text(game=self.game, text=str(self.nx), font_size=25, x=x + self.side,
                           y=y + self.sq * self.side / 2)  # TEXT NUMBER

        self.invisible_black_wall = wall

        # любой цвет выберем,
        # чтобы сливался с нашим фоном независимо от того какого цвета наш фон: розовый или черный

    def process_draw(self):
        self.number.process_draw()
        self.game.screen.blit(self.surface, (self.x, self.y))

    def get_neighbours(self):
        top_x = self.x
        top_y = self.y - 1

        bot_x = self.x
        bot_y = self.y + 1

        right_top_x = self.x - 1
        right_top_y = self.y

        left_top_x = self.x + 1
        left_top_y = self.y

        right_bot_x = self.x - 1
        right_bot_y = self.y + 1

        left_bot_x = self.x + 1
        left_bot_y = self.y + 1

        if not(self.even):
            right_top_x = self.x - 1
            right_top_y = self.y - 1

            left_top_x = self.x + 1
            left_top_y = self.y - 1

            right_bot_x = self.x - 1
            right_bot_y = self.y

            left_bot_x = self.x + 1
            left_bot_y = self.y

        # создадим список а, с коордами всех клеток. Обход с верхней клетки против часовой стрелки
        a = [ [top_x, top_y], [right_top_x, right_top_y], [right_bot_x, right_bot_y], [bot_x, bot_y], [left_bot_x, left_bot_y], [left_top_x, left_top_y]]
        return  a

    def set_color(self, color):
        self.color = color

    def return_color(self):
        return self.color

    def set_wall(self):
        self.invisible_black_wall = True
        self.color = self.black_color


class GridTileModel(DrawObject):
    def __init__(self, game, hex_side=40, width=8, height=10, field_width=2000, delta = 4):
        random_unit_count = 0
        self.sq = 3 ** (1 / 2)
        extra = hex_side / 2 - delta * self.sq
        self.hex_draw_array = [[0] * (width+2) for i in range(height+2)]
        self.height = height
        self.width = width
        for row in range(self.height+2):
            for collumn in range(self.width+2):
                random_unit_count = randint(0, 60)
                if row == 0 or row == self.height+2 or collumn == 0 or collumn == self.width+2:
                    self.hex_draw_array[row][collumn]=(GridTile(game,
                                                        collumn,
                                                        row,
                                                        hex_side,
                                                        random_unit_count,
                                                        (True if row % 2 == 0 else False),
                                                        collumn * (hex_side * 4 - 2 * extra),
                                                        row * (self.sq * hex_side / 2 + delta),
                                                        True,
                                                        Color.BLACK)
                                                )
                else:
                    self.hex_draw_array[row][collumn]=(GridTile(game,
                                                    collumn,
                                                    row,
                                                    hex_side,
                                                    random_unit_count,
                                                    (True if row % 2 == 0 else False),
                                                    collumn * (hex_side * 4 - 2 * extra),
                                                    row * (self.sq * hex_side / 2 + delta),
                                                    False,
                                                    Color.WHITE
                                                    )
                                                )

        print(len(self.hex_draw_array))

    def inPolygon(self,x, y):
        for row in range(1,self.height+1):
            for collumn in range(1,self.width+1):
                if (y >= self.hex_draw_array[row][collumn].pos_y) and (y<=self.hex_draw_array[row][collumn].pos_y + self.sq * self.side)\
                        and (x >=self.hex_draw_array[row][collumn].pos_x) and (x <=self.hex_draw_array[row][collumn].pos_x + 1.5 * self.side):
                    cell = self.hex_draw_array[row][collumn]
                    return cell

    def getCell(self, x, y):
        if x == 0 or x == self.width+2 or y == 0 or y == self.height+2:
            return None
        for row in range(1, self.height + 1):
            for collumn in range(1, self.width + 1):
                if self.hex_draw_array[row][collumn].x == x and self.hex_draw_array[row][collumn].y == y:
                    return self.hex_draw_array[row][collumn]

    def getCellByColor(self,color):
        for row in range(1,self.height+1):
            for collumn in range(1,self.width+1):
                cell = self.hex_draw_array[row][collumn]
                if (cell.return_color() == color):
                    return cell
        return None

    def make_cells_white(self):
        for row in range(1,self.height+1):
            for collumn in range(1,self.width+1):
                self.hex_draw_array[row][collumn].set_color(Color.WHITE)

    def make_cell_red(self, x, y):
        cell = self.getCell(x,y)
        if not cell:
            return
        self.make_cells_white()
        cell.set_color(Color.RED)

    def make_cell_green(self,cell):
        cell.set_color(Color.GREEN)

    def make_cells_green(self,cell):
        neightbours = cell.get_neightbours()
        for row in range(1,self.height+1):
            for collumn in range(1,self.width+1):
                neightbours[row][collumn].set_color(Color.GREEN)

    def make_cell_orange(self,x,y):
        cell = self.getCell(x,y)
        cell.set_color(Color.ORANGE)

    def move_units(self,redcell,orangecell,value):
        if not redcell:
            return
        if not orangecell:
            return
        redcell.nx -= value
        orangecell.nx += value

