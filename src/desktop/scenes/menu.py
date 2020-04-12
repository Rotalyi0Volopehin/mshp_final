from src.desktop.constants import Color
from src.desktop.objects.button import Btn
from src.desktop.scenes.base import Scene
from src.core.game_eng.GRID__TILE.GridTileModel import GridTileModel

from src.core.game_eng.GRID__TILE.GridTileController import GridTileController

from src.core.game_eng.GRID__TILE.GridTileView import GridTileView

class MenuScene(Scene):
    def create_objects(self):
        grid_model = GridTileModel(self.game)
        self.grid_controller = GridTileController(grid_model)
        grid_view = GridTileView(grid_model, self.grid_controller)
        self.grid_controller.init_view(grid_view)
        grid_view.sync()
        self.objects = [grid_view]

    def set_main_scene(self):
        self.set_next_scene(self.game.MAIN_SCENE_INDEX)

    def process_event(self,event):
        self.grid_controller.process_event(event)

    def exit(self):
        self.game.game_over = True