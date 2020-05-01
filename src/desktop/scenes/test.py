from constants import Color
from objects.button import Btn
from scenes.base import Scene
from objects.hex import Hex
from objects.hex_grid import Grid


class TestScene(Scene):
    def create_objects(self):
        self.hex_grid= Grid(self.game)
        self.button_zoom_out = Btn(self.game, (350, 255, 100, 40), Color.WHITE, "Zoom out", self.zoom_out)
        self.button_zoom_in = Btn(self.game, (350, 355, 100, 40), Color.WHITE, "Zoom in", self.zoom_in)
        self.objects = [self.hex_grid, self.button_zoom_in, self.button_zoom_out]

    def zoom_out(self):
        self.hex_grid.set_side(min((self.game.width / self.hex_grid.width), (self.game.height / self.hex_grid.height)) / 2)

    def zoom_in(self):
        self.hex_grid.set_side(100)