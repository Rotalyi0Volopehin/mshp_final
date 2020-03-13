import pygame
from random import randint
from constants import Color

from objects.base import DrawObject


class Hex(DrawObject):
    def __init__(self, game, x=0, y=0, side=100, args=None):       # param -> переименовать
        super().__init__(game)
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

    def process_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.on_click(event)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.on_release(event)

    def process_draw(self):
        pygame.draw.polygon(self.surface, self.color, self.hex_points, 5)
        self.game.screen.blit(self.surface, (self.x, self.y))

    def on_click(self, event):
        if pygame.draw.polygon(self.surface, self.color, self.hex_points, 5).collidepoint(event.pos):
            self.color = Color.RED

    def on_release(self, event):
        pass