from constants import Color
from objects.base import DrawObject
from  game_eng.grid_mvc.grid_model import GridTile
from objects.button import Btn

class GridTileView(DrawObject):
    def __init__(self, game, model, controller):
        super().__init__(game)
        self.model = model
        self.controller = controller
        self.EMP = Btn(self.game, (30, 450, 100, 40), Color.WHITE, 'EMP', self.controller.set_ability_emp)
        self.Fish = Btn(self.game, (30, 500, 100, 40), Color.WHITE, 'Fishing', self.controller.set_ability_fishing)
        self.abilities = [self.EMP,self.Fish]

    def process_draw(self):
        for item in self.abilities:
            item.process_draw()
        for row in range(self.model.width):
            for column in range(self.model.height):
                self.model.hex_draw_array[row][column].process_draw()