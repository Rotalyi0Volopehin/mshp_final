import pygame
from random import randint
from constants import Color
from objects.text import Text
from objects.base import DrawObject


class GridTileView(DrawObject):
    def __init__(self, model, controller):
        self.model = model
        self.controller = controller


    def process_draw(self):
        self.number.process_draw()
        self.game.screen.blit(self.surface, (self.x, self.y))