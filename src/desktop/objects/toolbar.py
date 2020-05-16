import pygame as pg
from constants import Color
from objects.base import DrawObject
from objects.toolbar_cell import ToolBarCell


class ToolBar(DrawObject):
    def __init__(self, game, **kwargs):
        self.game = game
        super().__init__(game)
        self.cells = []
        self.geometry = (35, self.game.height - 100, self.game.width - 70, 80)
        self.process_kwargs(kwargs)
        self.init_cells()

    def process_kwargs(self, kwargs):
        self.functions = {
            "K_1": None,
            "K_2": None,
            "K_3": None,
            "K_4": None,
            "K_5": None,
            "K_6": None,
            "K_7": None,
            "K_8": None,
            "K_9": None,
            "K_0": None,
        }
        for key, func in kwargs.items():
            if key in self.functions:
                self.functions[key] = func

    def init_cells(self):
        for i in range(10):
            function = self.functions["K_" + str((i+1) % 10)]
            self.cells.append(ToolBarCell(self.game, 35 + i * 74, self.game.height - 100,
                                          64, 64, (i + 1) % 10, function))
        self.cells[0].set_img('images/EMP.png')
        self.cells[1].set_img('images/Phishing.png')

    def process_event(self, event):
        if event.type == pg.KEYDOWN:
            st = str(event.key)
            n = int(st) - 48
            if n == 0:
                n = 9
            else:
                n -= 1
            if 9 >= n >= 0:
                self.cells[n].process_event(event)
        if event.type == pg.MOUSEBUTTONDOWN:
            for item in self.cells:
                item.process_event(event)

    def process_draw(self):
        for item in self.cells:
            item.process_draw()
