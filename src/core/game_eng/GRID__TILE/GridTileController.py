import pygame
from random import randint
from constants import Color
from objects.text import Text
from objects.base import DrawObject


class GridTileController():
    def __init__(self, game, model, view):
        self.game = game
        self.model = model
        self.view = view

    def process_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.on_click(event)

    def on_click(self, event):
        if self.model.inPolygon(event.pos[0], event.pos[1]) == 1:
