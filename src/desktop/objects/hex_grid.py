import pygame
from constants import Color
from random import *
from objects.base import DrawObject
from objects.hex import Hex
from objects.text import Text

class Grid(DrawObject):
    def __init__(self, game, hex_side=40, width=8, height=10, field_width=2000, delta = 4):
        super().__init__(game)
        self.game = game
        self.width = width
        self.height = height
        self.field_width = field_width
        self.hexes_array = []
        self.hex_side = hex_side
        self.sq = 3 ** (1 / 2)
        self.delta = delta
        self.extra = self.hex_side / 2 - self.delta * self.sq
        self.set_grid()
        self.last_red = None

    def process_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.on_click(event)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.on_release(event)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
            self.add_units(1)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
            self.add_units(-1)

    def set_grid(self):
        j = 0
        i = 0
        for row in range(self.height):
            for obj in range(self.width):
                j = randint(0, 60)
                i += 1
                if row % 2 == 0:
                    self.hexes_array.append(Hex(self.game,
                                                obj * (self.hex_side * 4 - 2 * self.extra),
                                                row * (self.sq * self.hex_side / 2 + self.delta),
                                                self.hex_side,
                                                i,
                                                nx=j,
                                                even=True,
                                                grid=self)
                                            )
                else:
                    self.hexes_array.append(Hex(self.game,
                                                2 * self.hex_side + (4 * self.hex_side) * obj - (2 * (obj + 1) - 1) * self.extra,
                                                self.sq * self.hex_side / 2 + (row - 1) * (self.sq * self.hex_side / 2 + self.delta) + self.delta,
                                                self.hex_side,
                                                i,
                                                nx=j,
                                                even=False,
                                                grid=self)
                                            )
        print(len(self.hexes_array))

    def process_draw(self):
        for item in self.hexes_array:
            item.process_draw()
            if item.is_red_color():  # покраска в красный, и ближайших соседей в зеленый, нужен фикс с крайними боковыми ячейками
                current_number_hex = item.get_number() - 1
                even = self.hexes_array[current_number_hex].get_even()
                top = item.get_number() - 17
                right_top = (item.get_number() - 10) if even else (item.get_number() - 9)
                left_top = (item.get_number() - 9) if even else (item.get_number() - 8)
                left_bot = (item.get_number() + 6) if even else (item.get_number() + 8)
                right_bot = (item.get_number() + 7) if even else (item.get_number() + 7)
                bot = item.get_number() + 15

                if item.get_number()==1:
                    left_bot = right_bot
                if item.get_number()==len(self.hexes_array):
                    left_top = right_top
                if (item.get_number()-1) % 16 == 0:
                    print(item.get_number())
                    right_top = left_top
                    left_bot = right_bot
                if item.get_number()% 16 == 0:
                    left_top = right_top
                    left_bot = right_bot

                self.erase_green()

                if len(self.hexes_array) - 1 >= top >= 0:
                    self.hexes_array[top].make_possible()

                if len(self.hexes_array) - 1 >= right_top >= 0:
                    self.hexes_array[right_top].make_possible()

                if len(self.hexes_array) - 1 >= left_top >= 0:
                    self.hexes_array[left_top].make_possible()

                if len(self.hexes_array) - 1 >= right_bot >= 0:
                    self.hexes_array[right_bot].make_possible()

                if len(self.hexes_array) - 1 >= left_bot >= 0:
                    self.hexes_array[left_bot].make_possible()

                if len(self.hexes_array) - 1 >= bot >= 0:
                    self.hexes_array[bot].make_possible()

    def set_side(self, new_side_size):
        self.hexes_array.clear()
        self.hex_side = new_side_size
        self.set_grid()

    def zoom_in(self, scale):
        self.hexes_array.clear()
        if self.hex_side + scale >= 14:
            self.hex_side += scale
        self.set_grid()

    def on_click(self, event):
        for item in self.hexes_array:
            item.process_draw()
            item.process_event(event)

    def erase_green(self):
        for item in self.hexes_array:
            if item.color == Color.GREEN:
                item.color = Color.WHITE
                item.redraw()

    def on_release(self, event):
        pass

    def find_red(self):
        for item in self.hexes_array:
            if item.is_red_color():
                return item.get_number() - 1

    def change_num(self, adress1,adress2, number):
        if adress1!=None and adress2!=None:
            if self.hexes_array[adress1].nx+number>=0 and self.hexes_array[adress2].nx-number>=0:
                self.hexes_array[adress1].nx += number
                self.hexes_array[adress2].nx -= number
                self.game.sfx_player.play_sound('HighBeep')

    def change_text(self, adress, number):
        self.hexes_array[adress].number = Text(game=self.game, text=number, font_size=25,
                                               x=self.hexes_array[adress].x+self.hex_side,
                                               y=self.hexes_array[adress].y+self.sq * self.hex_side / 2) # TEXT NUMBER

    def add_units(self, units):
        orange_adress = None
        for item in self.hexes_array:
            if item.color == Color.ORANGE:
                orange_adress = item.get_number() - 1
        red_adress = self.last_red
        if orange_adress != None and red_adress != None:
            self.change_num(orange_adress,red_adress, units)
            self.change_text(orange_adress, self.hexes_array[orange_adress].nx)
            self.change_text(red_adress, self.hexes_array[red_adress].nx)