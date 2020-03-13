import pygame
from random import randint
from constants import Color
from network_confrontation.src.desktop.objects.text import Text
from objects.base import DrawObject


class Hex(DrawObject):
    def __init__(self, game, x=0, y=0,  side=100, number=0, args=None, nx = 0, even = False):       # param -> переименовать
        super().__init__(game)
        self.even = even # чет нечет строчка
        self.nx = nx # номер
        self.x = x
        self.y = y
        self.side = side
        self.args = args
        self.color = Color.WHITE
        self.sq = 3 ** (1 / 2)
        self.hex_points = [(self.side / 2, 0),
                           (1.5 * self.side, 0),
                           (2 * self.side, self.sq * self.side / 2),
                           (1.5 * self.side, self.sq * self.side),
                           (self.side / 2, self.sq * self.side),
                           (0, self.sq * self.side / 2)]
        self.surface = pygame.Surface((2 * self.side, 2 * self.side))
        self.surface.set_colorkey(Color.BLACK)
        self.NUM = number # число юнитов
        self.number = Text(game=self.game, text=self.nx, font_size=25, x=x+19, y=y+18) # TEXT NUMBER

    def process_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.on_click(event)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.on_release(event)

    def process_draw(self):
        pygame.draw.polygon(self.surface, self.color, self.hex_points, 5)
        self.number.process_draw()
        self.game.screen.blit(self.surface, (self.x, self.y))

    def inPolygon(self,x, y):
        c = 0
        if (y >= self.y) and (y<=self.y + self.sq * self.side)\
                and (x >=self.x) and (x <=self.x + 1.5 * self.side):
            c = 1 - c
        return c

    def on_click(self, event):
        if self.inPolygon(event.pos[0], event.pos[1]) == 1:
            self.color = Color.RED

    def get_number(self):
        return self.NUM

    def is_red_color(self):
        return True if self.color == Color.RED else False

    def get_even(self):
        return self.even

    def make_possible(self):
        self.color = Color.GREEN

    def on_release(self, event):
        pass