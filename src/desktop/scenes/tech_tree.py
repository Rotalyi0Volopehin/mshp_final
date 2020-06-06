import pygame
import os

from objects.btn_img import ImageButton
from objects.current_player_plate import CurrentPlayerPlate
from objects.end_turn_button import EndTurnButton
from scenes.base import Scene
from objects.button import Btn
from constants import Color
from objects.grid_tile_info_plate import GridTileInfoPlate
from game_vc.grid_tile_vc import GridTileVC
from game_eng.grid_tile_upgrade_tree import GridTileUpgradeTree


class TreeScene(Scene):
    @staticmethod
    def upload_images(length):
        images = list()
        for i in range(length):
            images.append(pygame.image.load(os.path.join("images", f"Color{i + 1}.png")))
        return images

    def create_objects(self):
        self.width = self.game.width
        self.height = self.game.height
        self.types = GridTileUpgradeTree.tile_upgrade_bases
        self.game_vc = self.game.current_scene.game_vc
        self.objects.append(self.game_vc)
        self.add_buttons()
        #self.images = TreeScene.upload_images(len(self.types))
        button_back = Btn(self.game, (self.width - 240, 5, 100, 40), Color.WHITE, 'Карта',
                          self.game.return_to_upper_scene)
        self.objects.append(button_back)
        grid_tile_info_plate = GridTileInfoPlate(self.game, self.width - 20, 50, 340)

        self.end_turn_button = EndTurnButton(self.game, self.width - 100, self.height - 200)
        self.objects.append(self.end_turn_button)
        self.current_player_plate = CurrentPlayerPlate(self.game, self.width - 90, self.height - 183)
        self.objects.append(self.current_player_plate)

        self.objects.append(grid_tile_info_plate)

    def add_buttons(self):
        tech_pos = 0
        vertical_move_count = 1
        tile_centered = True  # GridTile должен быть сверху посередине
        f_button = False
        for upgrade_index in self.types:
            if not (f_button):
                pass
                f_button = True
            else:
                if self.is_central(upgrade_index) or tile_centered:
                    tile_centered = False
                    tech_pos = 0
                    btn = self.create_button(tech_pos, vertical_move_count, upgrade_index)
                    self.objects.append(btn)
                    tech_pos = -2
                    vertical_move_count += 1
                else:
                    tech_pos += 1
                    if tech_pos == 0:
                        tech_pos += 1
                    btn = self.create_button(tech_pos, vertical_move_count, upgrade_index)
                    self.objects.append(btn)

    def create_button(self, i, J, upgrade_index):
        y_move = 90
        x_move = 150
        img = (pygame.image.load(os.path.join("images", f"Color{1}.png")))
        #img = self.images[upgrade_index]
        x = self.width // 3 + x_move * i
        y = -30 + y_move * J
        img = pygame.transform.scale(img, (1, 1))
        return ImageButton(self.game, img, (x, y, 100, 40), str(upgrade_index)[-20:-2:], self.upgrade_as_none(upgrade_index))

    def is_central(self, index):
        if str(index).find("Enhanced") != -1:  # даже не пытайтесь найти ключ GridTile, не поможет
            return True

    def upgrade_as_none(self, type):
        def upgrade():
            tile = self.game_vc.grid_vc.selected_tile
            if tile.team == self.current_player_plate.team:
                GridTileUpgradeTree.upgrade_tile(tile, type)
                new_tile = self.game_vc.model.grid.tiles[tile.loc_x][tile.loc_y]
                GridTileVC(new_tile, self.game, tile.view.status)
                if self.game_vc.grid_vc.target_tile == tile:
                    self.game_vc.grid_vc.target_tile = new_tile
                self.game_vc.grid_vc.selected_tile = new_tile
        return upgrade
