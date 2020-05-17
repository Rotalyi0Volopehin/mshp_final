import exceptions
import pygame

from queue import Queue
from constants import Color
from geometry_tools import rect_contains_point, triangle_contains_point


class Hexagon:
    TOP_LEFT_POINT_INDEX = 0
    TOP_MID_POINT_INDEX = 1
    TOP_RIGHT_POINT_INDEX = 2
    BOTTOM_RIGHT_POINT_INDEX = 3
    BOTTOM_MID_POINT_INDEX = 4
    BOTTOM_LEFT_POINT_INDEX = 5
    SQ = 3 ** 0.5

    def __init__(self, side: int):
        if not isinstance(side, int):
            raise exceptions.ArgumentTypeException()
        self.side = side
        self.points = [
            (0, side >> 1),
            (side, 0),
            (side << 1, side >> 1),
            (side << 1, int(1.5 * side)),
            (side, side << 1),
            (0, int(1.5 * side)),
        ]
        self.__surfaces = dict()

    @property
    def top_left_point(self) -> tuple:
        return self.points[Hexagon.TOP_LEFT_POINT_INDEX]

    @property
    def top_mid_point(self) -> tuple:
        return self.points[Hexagon.TOP_MID_POINT_INDEX]

    @property
    def top_right_point(self) -> tuple:
        return self.points[Hexagon.TOP_RIGHT_POINT_INDEX]

    @property
    def bottom_left_point(self) -> tuple:
        return self.points[Hexagon.BOTTOM_LEFT_POINT_INDEX]

    @property
    def bottom_mid_point(self) -> tuple:
        return self.points[Hexagon.BOTTOM_MID_POINT_INDEX]

    @property
    def bottom_right_point(self) -> tuple:
        return self.points[Hexagon.BOTTOM_RIGHT_POINT_INDEX]

    def contains_point(self, x: int, y: int) -> bool:
        if not (isinstance(x, int) and isinstance(y, int)):
            raise exceptions.ArgumentTypeException()
        return rect_contains_point(self.top_left_point, self.top_right_point, self.bottom_left_point, x, y) or \
               triangle_contains_point(self.top_left_point, self.top_right_point, self.top_mid_point, x, y) or \
               triangle_contains_point(self.bottom_left_point, self.bottom_mid_point, self.bottom_right_point, x, y)

    def get_surface(self, edge_color: tuple, fill_color: tuple) -> pygame.Surface:
        if not (isinstance(edge_color, tuple) and isinstance(fill_color, tuple)):
            raise exceptions.ArgumentTypeException()
        hash_ = Hexagon.__calc_hash_of_colors(edge_color, fill_color)
        if hash_ not in self.__surfaces:
            return self.__render_surface(edge_color, fill_color, hash_)
        return self.__surfaces[hash_]

    def __render_surface(self, edge_color, fill_color, hash_):
        surface = pygame.Surface((2 * self.side, 2 * self.side))
        surface.set_colorkey(Color.BLACK)
        pygame.draw.polygon(surface, fill_color, self.points)
        pygame.draw.polygon(surface, edge_color, self.points, 3)
        self.__surfaces[hash_] = surface
        return surface

    @staticmethod
    def __calc_hash_of_colors(edge_color: tuple, fill_color: tuple) -> int:
        hash_ = 0
        for i in range(6):
            hash_ <<= 8
            hash_ |= edge_color[i] if i < 3 else fill_color[i - 3]
        return hash_
