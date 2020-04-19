from constants import Color
from game_eng.GRID__TILE.grid_controller import GridTileController
from game_eng.GRID__TILE.grid_model import GridModel
from game_eng.GRID__TILE.grid_view import GridTileView
from objects.button import Btn
from scenes.base import Scene


class MapScene(Scene):
    def create_objects(self):
        grid_model = GridModel(self.game)
        self.grid_controller = GridTileController(grid_model)
        grid_view = GridTileView(self.game, grid_model, self.grid_controller)
        self.grid_controller.init_view(grid_view)
        grid_view.process_draw()
        self.button_back = Btn(self.game, (350, 500, 100, 40), Color.WHITE, 'Меню', self.back_to_menu)
        self.objects = [grid_view,self.button_back]

    def process_current_event(self, event):
        self.grid_controller.process_event(event)


    def back_to_menu(self):
        self.set_next_scene(self.game.MENU_SCENE_INDEX)

    def exit(self):
        self.game.game_over = True

