import pygame
import os

from objects.btn_img import ImageButton
from scenes.base import Scene
from objects.button import Btn
from constants import Color
from objects.grid_tile_info_plate import GridTileInfoPlate
from game_vc.grid_tile_vc import GridTileVC
from game_eng.grid_tile_upgrade_tree import GridTileUpgradeTree

from game_eng.grid_tile import GridTile
from game_eng.grid_tile_ders.enhanced_tile import EnhancedGridTile
from game_eng.grid_tile_ders.defense_tile import DefenseGridTile
from game_eng.grid_tile_ders.service_tile import ServiceGridTile
from game_eng.grid_tile_ders.enhanced_tile_plus import EnhancedGridTilePlus
from game_eng.grid_tile_ders.defense_tile_plus import DefenseGridTilePlus
from game_eng.grid_tile_ders.service_tile_plus import ServiceGridTilePlus


class TreeScene(Scene):

    def create_objects(self):
        self.width = self.game.width
        self.height = self.game.height
        button_back = Btn(self.game, (self.width - 120, 5, 100, 40), Color.WHITE, 'Карта',
                          self.game.return_to_upper_scene)
        self.objects.append(button_back)
        self.game_vc = self.game.current_scene.game_vc
        self.objects.append(self.game_vc)
        grid_tile_info_plate = GridTileInfoPlate(self.game, self.width - 20, 50, 340)
        self.objects.append(grid_tile_info_plate)
        self.types = GridTileUpgradeTree.tile_upgrade_bases
        self.add_buttons()

    def add_buttons(self):
        num = 1
        tech_pos = 0
        vertical_move_count = 1
        for p in range(len(self.types)):
            self.objects.append(0)
        zero_index = self.objects.index(0)
        flag = True # GridTile должен быть сверху посередине
        for upgrade_index in self.types:
            if self.is_central(upgrade_index) or flag:
                flag = False
                tech_pos = 0
                btn = self.create_button(tech_pos, vertical_move_count, num, upgrade_index)
                self.objects[zero_index] = btn
                tech_pos = -2
                vertical_move_count += 1
            else:
                tech_pos += 1
                if tech_pos == 0:
                    tech_pos += 1
                btn = self.create_button(tech_pos, vertical_move_count, num, upgrade_index)
                self.objects[zero_index] = btn

            zero_index += 1

    def create_button(self, i, J, num, upgrade_index):
        y_move = 90
        x_move = 150
        img = pygame.image.load(os.path.join("images", f"Color{num}.png"))
        x = self.width // 3 + x_move * i
        y = -30 + y_move * J
        img = pygame.transform.scale(img, (1, 1))
        #TODO: ыыыыы
        if str(upgrade_index) == "<class 'game_eng.grid_tile.GridTile'>":
            return ImageButton(self.game, img, (x, y, 100, 40), str(upgrade_index)[-20:-2:],
                               self.upgrade_as_none(self.types[DefenseGridTile]))                      # это Enhanced
        elif str(upgrade_index) == "<class 'game_eng.grid_tile_ders.enhanced_tile.EnhancedGridTile'>":
            return ImageButton(self.game, img, (x, y, 100, 40), str(upgrade_index)[-20:-2:],
                               self.upgrade_as_none(self.types[EnhancedGridTile]))
        elif str(upgrade_index) == "<class 'game_eng.grid_tile_ders.defense_tile.DefenseGridTile'>":
            return ImageButton(self.game, img, (x, y, 100, 40), str(upgrade_index)[-20:-2:],
                               self.upgrade_as_none(self.types[DefenseGridTile]))
        elif str(upgrade_index) == "<class 'game_eng.grid_tile_ders.service_tile.ServiceGridTile'>":
            return ImageButton(self.game, img, (x, y, 100, 40), str(upgrade_index)[-20:-2:],
                               self.upgrade_as_none(self.types[ServiceGridTile]))
        elif str(upgrade_index) == "<class 'game_eng.grid_tile_ders.enhanced_tile_plus.EnhancedGridTilePlus'>":
            return ImageButton(self.game, img, (x, y, 100, 40), str(upgrade_index)[-20:-2:],
                               self.upgrade_as_none(self.types[EnhancedGridTilePlus]))
        elif str(upgrade_index) == "<class 'game_eng.grid_tile_ders.defense_tile_plus.DefenseGridTilePlus'>":
            return ImageButton(self.game, img, (x, y, 100, 40), str(upgrade_index)[-20:-2:],
                               self.upgrade_as_none(self.types[DefenseGridTilePlus]))
        elif str(upgrade_index) == "<class 'game_eng.grid_tile_ders.service_tile_plus.ServiceGridTilePlus'>":
            return ImageButton(self.game, img, (x, y, 100, 40), str(upgrade_index)[-20:-2:],
                               self.upgrade_as_none(self.types[ServiceGridTilePlus]))

    def is_central(self, index):
        if str(index).find("Enhanced") != -1: # даже не пытайтесь найти ключ GridTile, не поможет
            return True

    def upgrade_as_none(self, type):
        self.upgrade(type)

    def upgrade(self, upgrade):
        print(upgrade)
        tile = self.game_vc.grid_vc.selected_tile
        GridTileUpgradeTree.upgrade_tile(tile, upgrade)
        new_tile = self.game_vc.model.grid.tiles[tile.loc_x][tile.loc_y]
        GridTileVC(new_tile, self.game, tile.view.status)
        if self.game_vc.grid_vc.target_tile == tile:
            self.game_vc.grid_vc.target_tile = new_tile
        self.game_vc.grid_vc.selected_tile = new_tile

