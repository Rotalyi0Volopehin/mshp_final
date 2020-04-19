import pygame
import time
import os
import random

pygame.init()


class Bar:
    def __init__(self, screen, x=0, y=0, max=100, min=0, height=100, weight=400, bgcolor=(120, 0, 120),
                 bcolor=(200, 200, 0), function=None):
        self.x = x
        self.function = function
        self.y = y
        self.max = max
        self.min = min
        self.height = height
        self.weight = weight
        self.screen = screen
        self.bgcolor = bgcolor
        self.bcolor = bcolor
        self.val = 50

    def process_draw(self):
        pygame.draw.rect(self.screen, self.bgcolor, (self.x, self.y, self.weight, self.height))
        pygame.draw.rect(self.screen, self.bcolor,
                         (self.x + 3, self.y + 3, (self.weight- 6) * (self.val / self.max), self.height - 6))

    def process_event(self, events):
        pass

    def set_val(self, val):
        self.val = val

    def process_logic(self):
        if self.val > self.max:
            self.function()
        else:
            self.setval()
