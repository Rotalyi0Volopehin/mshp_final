from constants import Color
from objects.image import Image
from vc_game_eng.grid_controller import GridTileController
from game_eng.grid_model import GridModel
from vc_game_eng.grid_view import GridTileView
from objects.button import Btn
from scenes.base import Scene


class MapScene(Scene):
    def create_objects(self):
        grid_model = GridModel(self.game)
        self.grid_controller = GridTileController(grid_model)
        self.grid_view = GridTileView(self.game, grid_model, self.grid_controller)
        self.grid_controller.init_view(self.grid_view)
        self.grid_view.process_draw()
        self.image_bg = Image(self.game, file_name='images/Background.png', x=0, y=0)
        self.button_back = Btn(self.game, (350, 500, 100, 40), Color.WHITE, 'Меню', self.back_to_menu)
        self.objects = [self.image_bg, self.grid_view, self.grid_controller, self.button_back]


    def back_to_menu(self):
        self.set_next_scene(self.game.MENU_SCENE_INDEX)

    def exit(self):
        self.game.game_over = True
