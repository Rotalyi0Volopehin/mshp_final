import pygame
from random import randint
from constants import Color
from objects.text import Text
from objects.base import DrawObject
import exceptions
from game_eng.game_object_model import GameObjectModel


class GridTile(DrawObject):
    # Возможные состояния игровой клетки:
    #   black - наша невидимая черная стена
    #   white - не выбрана
    #   red - выбрана
    #   green - соседняя с выбранной
    #   orange - та клетка, куда двигаем ОЧКИ ЮНИТЫ ВИРУСЫ БОТНЕТЫ ФАЙРВОЛЛЫ.
    #   МНЕ ВСЕ РАВНО. Я ПОЛЕ С КЛЕТКАМИ ПИШУ НА ОСНОВЕ САПЕРА.
    #   ПОТОМ СВОИ МЕХАНИКИ И ИДЕИ ТУДА ДОБАВЛЯЙТЕ И КРЕПИТЕ!!!!

    def __init__(self, game, x=0, y=0, side=100, number_units=0, even=False):
        super().__init__(game)
        self.even = even  # чет нечет строчка
        self.nx = number_units  # ранд количество юнитов
        self.x = x
        self.y = y

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

        #pygame.draw.polygon(self.surface, self.color, self.hex_points, 5)
        self.number = Text(game=self.game, text=self.nx, font_size=25, x=x + self.side,
                           y=y + self.sq * self.side / 2)  # TEXT NUMBER

        self.color = Color.WHITE
        self.invisible_black_wall = False
        self.black_color = Color.BLACK # любой цвет выберем,
        # чтобы сливался с нашим фоном независимо от того какого цвета наш фон: розовый или черный

    @property
    def loc_x(self):
        return self.x

    @property
    def loc_y(self):
        return self.y

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

        if not(even):
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

    def set_wall(self):
        self.invisible_black_wall = True
        self.color = self.black_color


class GridTileModel(DrawObject):
    def __init__(self, game, hex_side=40, width=8, height=10, field_width=2000, delta = 4):
        random_unit_count = 0
        sq = 3 ** (1 / 2)

        self.hex_draw_array = []
        for row in range(height):
            for obj in range(width):
                random_unit_count = randint(0, 60)
                self.hex_draw_array.append(GridTile(game,
                                                obj * (hex_side * 4 - 2 * extra),
                                                row * (sq * hex_side / 2 + delta),
                                                hex_side,
                                                number_units=random_unit_count,
                                                even = True if row % 2 == 0 else False,
                                                x = row,           # Координаты смещений x,y
                                                y = obj,           # https://habr.com/ru/post/319644/
                                                )
                                            )

        print(len(self.hexes_array))