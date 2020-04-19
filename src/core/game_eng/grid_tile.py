import pygame

from random import randint
from constants import Color
from objects.base import DrawObject
from objects.text import Text


# TODO: Андрей, что это значит? Это не модель!


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
