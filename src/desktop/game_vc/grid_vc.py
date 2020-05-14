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
        for column in self.model.tiles:
            for tile in column:
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
        for column in self.model.tiles:
            for tile in column:
                tile.view.process_draw()

    def process_event(self, event):
        for column in self.model.tiles:
            for tile in column:
                tile.controller.process_event(event)
        if (event.type == pygame.MOUSEBUTTONDOWN) and (4 <= event.button <= 5):
            self.__try_move_power(5 if event.button == 4 else -5)

    def __try_move_power(self, value):
        if self.selected_tile.power < value:
            value = self.selected_tile.power
        elif (value <= 0) and (self.selected_tile.team == self.target_tile.team) and (self.target_tile.power < -value):
            value = -self.target_tile.power
        self.selected_tile.move_power(self.target_tile, value)


    def on_scroll(self, value):
        self.selected_tile.move_power(self.target_tile, value)

    def use_ability_emp(self):
        self.model.ability_emp(self.target_tile)

    def use_ability_fishing(self):
        self.model.ability_fishing(self.target_tile)
