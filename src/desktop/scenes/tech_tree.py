from scenes.base import Scene
from objects.button import Btn
from objects.text import Text
from constants import Color
from objects.toolbar import ToolBar
from objects.end_turn_button import EndTurnButton
from objects.current_player_plate import CurrentPlayerPlate
from objects.grid_tile_info_plate import GridTileInfoPlate

class TreeScene(Scene):
    def create_objects(self):
        width = self.game.width
        height = self.game.height
        button_back = Btn(self.game, (width - 120, 5, 100, 40), Color.WHITE, 'Карта', self.game.return_to_upper_scene)
        self.objects.append(button_back)
        self.game_vc = self.game.current_scene.game_vc
        self.objects.append(self.game_vc)
        grid_tile_info_plate = GridTileInfoPlate(self.game, width - 20, 50, 340)
        self.objects.append(grid_tile_info_plate)

        