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
    #   orange - та клетка, куда двигаем ОЧКИ ЮНИТЫ ВИРУСЫ БОТНЕТЫ ФАЙРВОЛЛЫ и тд.

    def __init__(self, game, side, color, even, screen_x, screen_y, wall, y, x):
        super().__init__(game)
        self.even = even  # чет нечет строчка
        self.nx = randint(0, 60)  # ранд количество юнитов
        self.x = x  # координаты смещений
        self.y = y
        self.pos_x = screen_x  # на экране позиция
        self.pos_y = screen_y
        self.color = color
        self.side = side
        self.sq = 3 ** (1 / 2)
        self.hex_points = [(self.side / 2, 0),
                           (1.5 * self.side, 0),
                           (2 * self.side, self.sq * self.side / 2),
                           (1.5 * self.side, self.sq * self.side),
                           (self.side / 2, self.sq * self.side),
                           (0, self.sq * self.side / 2)]

        self.number = Text(game=self.game, text=str(self.nx), font_size=25, x=screen_x + self.side,
                           y=screen_y + self.sq * self.side / 2)
        self.invisible_black_wall = wall
        self.update_surface()

    def update_surface(self):
        self.surface = pygame.Surface((2 * self.side, 2 * self.side))
        self.surface.set_colorkey(Color.BLACK)
        self.number.update_text(str(self.nx))
        pygame.draw.polygon(self.surface, self.color, self.hex_points, 5)

    def process_draw(self):
        #self.update_surface()
        self.number.process_draw()
        self.game.screen.blit(self.surface, (self.pos_x, self.pos_y))

    def get_neighbours(self):  # чет-q
        top_x = self.x
        top_y = self.y - 1

        bot_x = self.x
        bot_y = self.y + 1

        left_top_x = self.x - 1
        left_top_y = self.y

        right_top_x = self.x + 1
        right_top_y = self.y

        right_bot_x = self.x - 1
        right_bot_y = self.y + 1

        left_bot_x = self.x + 1
        left_bot_y = self.y + 1

        if not (self.even):
            left_top_x = self.x - 1
            left_top_y = self.y - 1

            right_top_x = self.x + 1
            right_top_y = self.y - 1

            left_bot_x = self.x - 1
            right_bot_y = self.y

            right_bot_x = self.x + 1
            left_bot_y = self.y

        # создадим список а, с коордами всех клеток. Обход с верхней клетки против часовой стрелки
        a = [[top_x, top_y], [right_top_x, right_top_y], [right_bot_x, right_bot_y], [bot_x, bot_y],
             [left_bot_x, left_bot_y], [left_top_x, left_top_y]]
        return a

    def set_color(self, color):
        self.color = color
        self.update_surface()

    def return_color(self):
        return self.color

    def set_wall(self):
        self.invisible_black_wall = True
        self.color = self.black_color


class GridTileModel(DrawObject):
    def __init__(self, game, hex_side=40, width=8, height=10, delta=4):
        super().__init__(game)
        print("model added")
        self.sq = 3 ** (1 / 2)
        self.extra = hex_side / 2 - delta * self.sq
        self.hex_draw_array = [
            [0] * (width + 2) for i in range(height + 2)
        ]
        self.height = height
        self.width = width
        self.delta = delta
        i = -1  #x,y смещений
        j = 0
        for collumn in range(self.height + 2):  # нечет-q https://habr.com/ru/post/319644/
            i+=2
            for row in range(self.width + 2):
                j+=1
                if row == 0 or row == self.height + 2 \
                        or collumn == 0 or collumn == self.width + 2:
                    self.add_cell(game, hex_side, Color.BLACK, collumn, row, True,j,i)
                else:
                    self.add_cell(game, hex_side, Color.WHITE, collumn, row, False,j,i)

    def add_cell(self, game, hex_side, color, collumn, row, is_wall, y, x):
        self.hex_draw_array[collumn][row] = GridTile(
            game,
            hex_side,
            color,
            True if row % 2 ==0 else False,
            collumn * (hex_side * 4 - 2 * self.extra) if row % 2 == 0 else 2 * hex_side + (4 * hex_side) * collumn - (2 * (collumn + 1) - 1) * self.extra,
            row * (self.sq * hex_side / 2 + self.delta) if row % 2 == 0 else self.sq * hex_side / 2 + (row - 1) * (self.sq * hex_side / 2 + self.delta) + self.delta,
            is_wall,
            y-1 if row % 2 == 0 else y,
            math.floor(x / 2) if row % 2 == 0 else math.floor(x/2 - 1)
        )

    def inPolygon(self, x, y):
        for row in range(1, self.height + 1):
            for collumn in range(1, self.width + 1):
                if (y >= self.hex_draw_array[row][collumn].pos_y) and (
                        y <= self.hex_draw_array[row][collumn].pos_y + self.hex_draw_array[row][collumn].sq *
                        self.hex_draw_array[row][collumn].side) \
                        and (x >= self.hex_draw_array[row][collumn].pos_x) and (
                        x <= self.hex_draw_array[row][collumn].pos_x + 1.5 * self.hex_draw_array[row][collumn].side):
                    cell = self.hex_draw_array[row][collumn]
                    print(cell)
                    return cell

    def getCell(self, x, y):
        if x == 0 or x == self.width + 2 or y == 0 or y == self.height + 2:
            return None
        for row in range(1, self.height + 1):
            for collumn in range(1, self.width + 1):
                if self.hex_draw_array[row][collumn].x == x and self.hex_draw_array[row][collumn].y == y:
                    return self.hex_draw_array[row][collumn]

    def getCellByColor(self, color):
        for row in range(1, self.height + 1):
            for collumn in range(1, self.width + 1):
                cell = self.hex_draw_array[row][collumn]
                if (cell.return_color() == color):
                    return cell
        return None

    def make_cells_white(self):
        for row in range(1, self.height + 1):
            for collumn in range(1, self.width + 1):
                self.hex_draw_array[row][collumn].set_color(Color.WHITE)

    def make_cell_red(self, x, y):
        cell = self.getCell(x, y)
        if not cell:
            return
        self.make_cells_white()
        cell.set_color(Color.RED)

    def make_cell_green(self, cell):
        cell.set_color(Color.GREEN)

    def make_cells_green(self, cell):
        neightbours = cell.get_neighbours()
        print("KLETKA", cell.x, cell.y)
        for row in range(6):
            print(neightbours[row][0], neightbours[row][1])
            self.make_cell_green(self.hex_draw_array[neightbours[row][0]][neightbours[row][1]])

    def make_cell_orange(self, x, y):
        cell = self.getCell(x, y)
        cell.set_color(Color.ORANGE)

    def move_units(self, redcell, orangecell, value):
        if not redcell:
            return
        if not orangecell:
            return
        redcell.nx -= value
        orangecell.nx += value
