import pygame
from random import randint
from constants import Color
from random import *
from objects.base import DrawObject
from objects.hex import Hex


class Grid(DrawObject):
    def __init__(self, game, hex_side=40, width=8, height=10, field_width=2000):
        super().__init__(game)
        self.game = game
        self.width = width
        self.height = height
        self.field_width = field_width
        self.hexes_array = []
        self.hex_side = hex_side
        self.sq = 3 ** (1 / 2)
        self.set_grid()

    def process_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.on_click(event)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.on_release(event)
        #TODO: we need a camera. Чтобы когда скролил игрок ,она изменяла масштаб там, где курсор мыши. Ну как норм люди, картинку приблиэают, удалают
        """
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
            self.zoom_in(2)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
            self.zoom_in(-2)
        """
    def set_grid(self):
        for row in range(self.height):
            for obj in range(self.width):
                i = randint(0,60)
                if row % 2 == 0:
                    self.hexes_array.append(Hex(self.game,
                                                3*obj*self.hex_side,
                                                row * self.sq * self.hex_side / 2,
                                                self.hex_side,
                                                i)
                                                )
                else:
                    self.hexes_array.append(Hex(self.game,
                                                1.5 * self.hex_side + 3 * self.hex_side * obj,
                                                self.sq * self.hex_side / 2 + (row - 1) * self.sq * self.hex_side / 2,
                                                self.hex_side,
                                                i)
                                                )
        print(len(self.hexes_array))

    def process_draw(self):
        for obj in self.hexes_array:
            obj.process_draw()

    def set_side(self, new_side_size):
        self.hexes_array.clear()
        self.hex_side = new_side_size
        self.set_grid()

    def zoom_in(self, scale):
        self.hexes_array.clear()
        if self.hex_side+scale >= 14:
            self.hex_side += scale
        self.set_grid()

    def on_click(self, event):
        print(event.pos)
        for item in self.hexes_array:
            item.process_event(event)

    def on_release(self, event):
        pass
