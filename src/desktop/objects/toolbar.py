import pygame

from game_eng.market import Market
from objects.base import DrawObject
from objects.toolbar_cell import ToolBarCell


class ToolBar(DrawObject):
    def __init__(self, game, geometry: tuple):
        super().__init__(game)
        self.cells = []
        self.geometry = geometry
        self.__init_tools()
        self.__init_cells()

    def __init_tools(self):
        self.tools = dict()
        i = 0
        for pt_type in Market.tool_types:
            self.tools["K_" + str(i)] = pt_type()
            i += 1

    def __init_cells(self):
        for i in range(10):
            num = (i + 1) % 10
            key = "K_" + str(num)
            tool = self.tools[key] if key in self.tools else None
            x = self.geometry[0] + i * 74
            y = self.geometry[1]
            self.cells.append(ToolBarCell(self.game, x, y, 64, 64, num, tool))

    def process_event(self, event):
        if event.type == pygame.KEYUP:
            num = event.key - 48
            if num == 0:
                num = 9
            else:
                num -= 1
            if 9 >= num >= 0:
                self.cells[num].process_event(event)
        else:
            for item in self.cells:
                item.process_event(event)

    def process_draw(self):
        for item in self.cells:
            item.process_draw()
