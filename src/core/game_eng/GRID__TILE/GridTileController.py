import pygame
from random import randint
from src.desktop.constants import Color
from src.desktop.objects.text import Text
from src.desktop.objects.base import DrawObject


class GridTileController():
    def __init__(self, model):
        self.model = model

    def init_view(self,view):
        self.view = view

    def process_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.on_click(event)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
            self.on_scroll(1)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
            self.on_scroll(-1)

    def on_click(self, event):
        clicked_cell = self.model.inPolygon

        if clicked_cell.return_color() == Color.WHITE:
            self.model.make_cells_white()
            self.model.make_cell_red(clicked_cell.x,clicked_cell.y)
            self.model.make_cells_green(clicked_cell)
        elif clicked_cell.return_color() == Color.RED:
            self.model.make_cells_white()
        elif clicked_cell.return_color() == Color.GREEN:
            self.model.make_cell_orange(clicked_cell.x,clicked_cell.y)
        elif clicked_cell.return_color() == Color.ORANGE:
            self.model.make_cell_green(clicked_cell)
        print("OK")
        self.view.sync()

    def on_scroll(self,value):
        self.model.move_units(self.model.getCellByColor(Color.RED),self.model.getCellByColor(Color.ORANGE),value)
        self.view.sync()