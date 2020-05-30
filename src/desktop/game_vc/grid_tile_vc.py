import pygame

from enum import Enum
from game_vc.hexagon import Hexagon
from game_eng.grid_tile import GridTile
from constants import Color
from objects.base import DrawObject
from objects.text import Text
from game_vc.grid_tile_sprite_extender import GridTileSpriteExtender


class GridTileVCStatus(Enum):
    DEFAULT = Color.WHITE  # не выбрана
    SELECTED = Color.MAGENTA  # выбрана
    TARGET = Color.ORANGE  # та клетка, куда двигаем все, что хотим
    CHANGED = Color.CYAN  # изменена игроком


class GridTileVC(DrawObject):
    HEXAGON = Hexagon(20)
    DIST_BETWEEN_TILES = 3

    def __init__(self, model: GridTile, game, status):
        super().__init__(game)
        self.model = model
        model.set_view(self)
        model.set_controller(self)
        self.pos_x, self.pos_y = self.pos = self.__calc_screen_pos()
        self.status = status
        self.__surface = None
        self.__surface_team = model.team
        self.__surface_status = None
        self.__init_surface()

    def __init_surface(self):
        side = GridTileVC.HEXAGON.side
        sq = Hexagon.SQ
        self.number = Text(game=self.game, text=str(self.model.power), font_size=20, x=self.pos_x + side,
                           y=self.pos_y + sq * side / 2)
        self.render_number()
        self.update_surface()

    def __calc_screen_pos(self):
        side = GridTileVC.HEXAGON.side
        sq = Hexagon.SQ
        x = self.model.loc_x
        y = self.model.loc_y
        pos_x = x * (GridTileVC.DIST_BETWEEN_TILES + (side << 1))
        if self.model.odd_row:
            pos_x += side
        pos_y = y * int(1.5 * (side + GridTileVC.DIST_BETWEEN_TILES))
        return int(pos_x), int(pos_y)

    def contains_point(self, x: int, y: int) -> bool:
        return GridTileVC.HEXAGON.contains_point(x - self.pos_x, y - self.pos_y)

    def render_number(self):
        self.number.update_text("{:0>2x}".format(self.model.power))

    def update_surface(self):
        if (self.__surface_status != self.status) or (self.__surface_team != self.model.team):
            from game_vc.game_vc import GameVC
            fill_color = GameVC.get_team_color(self.model.team)
            self.__surface = GridTileVC.HEXAGON.get_surface(self.status.value, fill_color)
            self.__surface_status = self.status
            self.__surface_team = self.model.team

    def process_draw(self):
        self.render_number()
        self.update_surface()
        self.game.screen.blit(self.__surface, self.pos)
        self.number.process_draw()
        GridTileSpriteExtender.extend_sprite(self, self.game.screen)

    def process_event(self, event):
        mouse_down = event.type == pygame.MOUSEBUTTONDOWN
        mouse_up = event.type == pygame.MOUSEBUTTONUP
        if (mouse_down or mouse_up) and (event.button == 1):
            x = int(event.pos[0])
            y = int(event.pos[1])
            if self.contains_point(x, y):
                grid_view = self.model.grid.view
                if mouse_down:
                    grid_view.select_target_tile(None)
                    grid_view.select_tile(self.model)
                elif (self.model == grid_view.selected_tile) or \
                        (self.model in grid_view.selected_tile.get_neighbours()):
                    grid_view.select_target_tile(self.model)
