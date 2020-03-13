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
        j = 0
        i = 0
        for row in range(self.height):
            for obj in range(self.width):
                j = randint(0,60)
                i += 1
                if row % 2 == 0:
                    self.hexes_array.append(Hex(self.game,
                                                3*obj*self.hex_side,
                                                row * self.sq * self.hex_side / 2,
                                                self.hex_side,
                                                i,
                                                nx=j,
                                                even=True)
                                                )
                else:
                    self.hexes_array.append(Hex(self.game,
                                                1.5 * self.hex_side + 3 * self.hex_side * obj,
                                                self.sq * self.hex_side / 2 + (row - 1) * self.sq * self.hex_side / 2,
                                                self.hex_side,
                                                i,
                                                nx=j,
                                                even=False)
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
            item.color = Color.WHITE

        for item in self.hexes_array:
            item.process_event(event)

            if item.is_red_color() == True:
                current_number_hex = item.get_number()-1
                even = self.hexes_array[current_number_hex].get_even()
                print(current_number_hex)
                print(even)
                top = item.get_number() - 17
                right_top = (item.get_number() - 10) if even else (item.get_number() - 9)
                left_top = (item.get_number() - 9) if even else (item.get_number() - 8)
                left_bot = (item.get_number() + 6) if even else (item.get_number() + 8)
                right_bot = (item.get_number() + 7) if even else (item.get_number() + 7)
                bot = item.get_number() + 15
                print(top+1, right_top+1, left_top+1, right_bot+1, left_bot+1, bot+1)
                if len(self.hexes_array)-1 >=top>=0:
                    self.hexes_array[top].make_possible()

                if len(self.hexes_array)-1 >=right_top>=0:
                    self.hexes_array[right_top].make_possible()

                if len(self.hexes_array)-1 >=left_top>=0:
                    self.hexes_array[left_top].make_possible()

                if len(self.hexes_array)-1 >=right_bot>=0:
                    self.hexes_array[right_bot].make_possible()

                if len(self.hexes_array)-1 >=left_bot>=0:
                    self.hexes_array[left_bot].make_possible()

                if len(self.hexes_array)-1 >= bot >=0:
                    self.hexes_array[bot].make_possible()
                    print(self.hexes_array[bot].color)


    def on_release(self, event):
        pass
