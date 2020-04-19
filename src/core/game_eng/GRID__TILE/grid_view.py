from objects.base import DrawObject
from  game_eng.GRID__TILE.grid_model import GridTile

class GridTileView(DrawObject):
    def __init__(self, game, model, controller):
        super().__init__(game)
        self.model = model
        self.controller = controller

    def process_draw(self):
        for row in range(self.model.width):
            for column in range(self.model.height):
                self.model.hex_draw_array[row][column].process_draw()
