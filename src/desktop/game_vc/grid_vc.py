import exceptions
import pygame

from game_eng.grid_model import GridModel
from game_vc.grid_tile_vc import GridTileVC, GridTileVCStatus
from objects.base import DrawObject


class GridVC(DrawObject):
    def __init__(self, model: GridModel, game):
        super().__init__(game)
        self.model = model
        model.set_view(self)
        model.set_controller(self)
        self.selected_tile = self.target_tile = None
        self.__add_vc_to_tile_matrix()

    def __add_vc_to_tile_matrix(self):
        for tile in self.model.foreach():
            GridTileVC(tile, self.game, GridTileVCStatus.DEFAULT)

    def get_tile_by_pos_on_screen(self, pos_x, pos_y):
        raise exceptions.NotImplementedException()

    def select_tile(self, tile):
        if self.selected_tile is not None:
            self.selected_tile.view.status = GridTileVCStatus.DEFAULT
        self.selected_tile = tile
        if tile is not None:
            tile.view.status = GridTileVCStatus.SELECTED

    def select_target_tile(self, tile):
        if self.target_tile is not None:
            self.target_tile.view.status = GridTileVCStatus.DEFAULT
        self.target_tile = tile
        if tile is not None:
            tile.view.status = GridTileVCStatus.TARGET

    def process_draw(self):
        for tile in self.model.foreach():
            tile.view.process_draw()

    def process_event(self, event):
        for tile in self.model.foreach():
            tile.controller.process_event(event)
        if (event.type == pygame.MOUSEBUTTONDOWN) and (4 <= event.button <= 5):
            self.__try_move_power(4 if event.button == 4 else -4)
        elif event.type == pygame.KEYUP:
            self.__handle_key_up(event.key)

    def __handle_key_up(self, key):
        selected = self.selected_tile
        target = self.target_tile
        if key == pygame.K_c:
            self.select_tile(None)
            self.select_target_tile(None)
        elif (selected is not None) and (target is not None):
            if key == pygame.K_END:
                self.__move_power(selected.power)
            elif key == pygame.K_HOME:
                if selected.team == target.team:
                    self.__move_power(-target.power)
                else:
                    self.__move_power(-(selected.power_cap + target.power_cap), True)
            elif key == pygame.K_UP:
                self.__move_power(1)
            elif key == pygame.K_DOWN:
                self.__move_power(-1)
        if selected is not None:
            if key == pygame.K_F1:
                from game_eng.grid_tile_ders.enhanced_tile import EnhancedGridTile
                self.__try_upgrade_tile(EnhancedGridTile)
            elif key == pygame.K_F2:
                from game_eng.grid_tile_ders.defense_tile import DefenseGridTile
                self.__try_upgrade_tile(DefenseGridTile)
            elif key == pygame.K_F3:
                from game_eng.grid_tile_ders.service_tile import ServiceGridTile
                self.__try_upgrade_tile(ServiceGridTile)
            elif key == pygame.K_F4:
                from game_eng.grid_tile_ders.enhanced_tile_plus import EnhancedGridTilePlus
                self.__try_upgrade_tile(EnhancedGridTilePlus)
            elif key == pygame.K_F5:
                from game_eng.grid_tile_ders.defense_tile_plus import DefenseGridTilePlus
                self.__try_upgrade_tile(DefenseGridTilePlus)
            elif key == pygame.K_F6:
                from game_eng.grid_tile_ders.service_tile_plus import ServiceGridTilePlus
                self.__try_upgrade_tile(ServiceGridTilePlus)

    def __try_upgrade_tile(self, upgrade):
        from game_eng.grid_tile_upgrade_tree import GridTileUpgradeTree
        GridTileUpgradeTree.upgrade_tile(self.selected_tile, upgrade)
        new_tile = self.model.tiles[self.selected_tile.loc_x][self.selected_tile.loc_y]
        GridTileVC(new_tile, self.game, self.selected_tile.view.status)
        if self.target_tile == self.selected_tile:
            self.target_tile = new_tile
        self.selected_tile = new_tile

    def __try_move_power(self, value):
        if (self.selected_tile is None) or (self.target_tile is None):
            return
        self.__move_power(value, True)

    def __move_power(self, value, cut_surplus=False):
        team = self.game.current_scene.game_vc.model.current_team
        self.selected_tile.try_move_power_as_team(self.target_tile, value, team, cut_surplus)
