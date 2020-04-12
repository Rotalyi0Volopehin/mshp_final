import pygame
from random import randint
from src.desktop.constants import Color
from src.desktop.objects.text import Text
from src.desktop.objects.base import DrawObject


class GridTileView(DrawObject):
    def __init__(self, model, controller):
        print("view added")
        self.model = model
        self.controller = controller

    def process_draw(self):
        for row in range(self.model.height):
            for column in range(self.model.width):
                cell = self.model.getCell(row,column)
                if cell:
                    cell.process_draw()
