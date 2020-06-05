from scenes.base import Scene
from objects.button import Btn
from constants import Color
from objects.toolbar import ToolBar
from objects.end_turn_button import EndTurnButton
from objects.current_player_plate import CurrentPlayerPlate
from objects.grid_tile_info_plate import GridTileInfoPlate
from scenes.main_menu import MainMenuScene
from scenes.tech_tree import TreeScene


class MapScene(Scene):
    def __init__(self, game):
        super().__init__(game)


    def create_objects(self):
        width = self.game.width
        height = self.game.height
        button_back = Btn(self.game, (width - 120, 5, 100, 40), Color.WHITE, 'Меню', self.__set_menu_scene)
        self.objects.append(button_back)
        button_up = Btn(self.game, (width - 240, 5, 100, 40), Color.WHITE, 'Прокачка', self.__set_tech_scene)
        self.objects.append(button_up)
        self.game_vc = self.game.current_scene.game_vc
        self.objects.append(self.game_vc)
        toolbar_geom = (35, height - 100, width - 70, 80)
        self.toolbar = ToolBar(self.game, toolbar_geom)
        self.objects.append(self.toolbar)
        self.end_turn_button = EndTurnButton(self.game, width - 100, height - 200)
        self.objects.append(self.end_turn_button)
        current_player_plate = CurrentPlayerPlate(self.game, width - 90, height - 183)
        self.objects.append(current_player_plate)
        grid_tile_info_plate = GridTileInfoPlate(self.game, width - 20, 50, 340)
        self.objects.append(grid_tile_info_plate)

    def __set_menu_scene(self):
        self.game.goto_deeper_scene(MainMenuScene)

    def __set_tech_scene(self):
        self.game.goto_deeper_scene(TreeScene)