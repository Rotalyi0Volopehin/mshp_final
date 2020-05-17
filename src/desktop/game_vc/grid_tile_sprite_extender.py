import pygame
import exceptions

from constants import Color
from game_eng.grid_tile_ders.enhanced_tile import EnhancedGridTile
from game_eng.grid_tile_ders.defense_tile import DefenseGridTile
from game_eng.grid_tile_ders.service_tile import ServiceGridTile
from game_eng.grid_tile_ders.enhanced_tile_plus import EnhancedGridTilePlus
from game_eng.grid_tile_ders.defense_tile_plus import DefenseGridTilePlus
from game_eng.grid_tile_ders.service_tile_plus import ServiceGridTilePlus


def enhanced_ext(x, y, surface):
    pygame.draw.line(surface, Color.WHITE, (x - 2, y + 1), (x + 2, y + 1), 3)


def enhanced_ext_plus(x, y, surface):
    pygame.draw.rect(surface, Color.WHITE, (x - 2, y, 5, 6))


def defense_ext(x, y, surface):
    pygame.draw.polygon(surface, Color.WHITE, [(x - 2, y), (x + 2, y), (x, y + 4)])


def defense_ext_plus(x, y, surface):
    pygame.draw.polygon(surface, Color.WHITE, [(x - 4, y), (x + 4, y), (x, y + 6)])


def service_ext(x, y, surface):
    pygame.draw.polygon(surface, Color.WHITE, [(x - 2, y + 4), (x + 2, y + 4), (x, y)])


def service_ext_plus(x, y, surface):
    pygame.draw.polygon(surface, Color.WHITE, [(x - 4, y + 6), (x + 4, y + 6), (x, y)])


class GridTileSpriteExtender:
    @staticmethod
    def get_grid_tile_vc_type() -> type:
        if not hasattr(GridTileSpriteExtender, "__grid_tile_vc_type"):
            from game_vc.grid_tile_vc import GridTileVC
            GridTileSpriteExtender.__grid_tile_vc_type = GridTileVC
        return GridTileSpriteExtender.__grid_tile_vc_type

    @staticmethod
    def extend_sprite(grid_tile_vc, surface: pygame.Surface):
        grid_tile_vc_type = GridTileSpriteExtender.get_grid_tile_vc_type()
        if not (isinstance(grid_tile_vc, grid_tile_vc_type) and isinstance(surface, pygame.Surface)):
            raise exceptions.ArgumentTypeException()
        grid_type = type(grid_tile_vc.model)
        if grid_type in GridTileSpriteExtender.extensions:
            ext = GridTileSpriteExtender.extensions[grid_type]
            side = grid_tile_vc_type.HEXAGON.side
            x = grid_tile_vc.pos_x + side
            y = grid_tile_vc.pos_y + (side >> 2) + side
            ext(x, y, surface)

    extensions = {
        EnhancedGridTile: enhanced_ext,
        DefenseGridTile: defense_ext,
        ServiceGridTile: service_ext,
        EnhancedGridTilePlus: enhanced_ext_plus,
        DefenseGridTilePlus: defense_ext_plus,
        ServiceGridTilePlus: service_ext_plus,
    }
