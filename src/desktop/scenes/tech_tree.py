import pygame
import os
from scenes.base import Scene
from objects.button import Btn
from objects.text import Text
from constants import Color
from objects.toolbar import ToolBar
from objects.end_turn_button import EndTurnButton
from objects.current_player_plate import CurrentPlayerPlate
from objects.grid_tile_info_plate import GridTileInfoPlate
from objects.btn_img import ImageButton
from game_eng.grid_tile_ders.defense_tile import DefenseGridTile


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
        num = 1
        img = pygame.image.load(os.path.join("images", f"Color{num}.png"))
        img = pygame.transform.scale(img, (100, 40))
        tile = self.game.current_scene.game_vc.grid_vc.selected_tile
        #self.btn_1 = ImageButton(self.game, img, (10, 10, 100, 40), None,
        #                         (tile.upgrade(DefenseGridTile)))
        tile.upgrade(DefenseGridTile)
        self.objects.append(self.btn_1)
