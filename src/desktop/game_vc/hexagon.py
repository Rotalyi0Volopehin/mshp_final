import exceptions
import pygame

from queue import Queue
from constants import Color


def sign(value) -> int:
    if value > 0:
        return 1
    elif value < 0:
        return -1
    return 0


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
        return self.__rect_contains_p(self.top_left_point, self.top_right_point, self.bottom_left_point, x, y) or \
               self.__triangle_contains_p(self.top_left_point, self.top_right_point, self.top_mid_point, x, y) or \
               self.__triangle_contains_p(self.bottom_left_point, self.bottom_mid_point, self.bottom_right_point, x, y)

    @staticmethod
    def __rect_contains_p(origin, right_top, left_bottom, x, y) -> bool:
        return (origin[0] <= x) and (right_top[0] >= x) and (origin[1] <= y) and (left_bottom[1] >= y)

    @staticmethod
    def __triangle_contains_p(p1, p2, p3, x, y) -> bool:
        s1 = (p1[0] - x) * (p2[1] - p1[1]) - (p2[0] - p1[0]) * (p1[1] - y)
        s2 = (p2[0] - x) * (p3[1] - p2[1]) - (p3[0] - p2[0]) * (p2[1] - y)
        s3 = (p3[0] - x) * (p1[1] - p3[1]) - (p1[0] - p3[0]) * (p3[1] - y)
        return (sign(s1) == sign(s2)) and (sign(s2) == sign(s3))

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
        self.__flood_fill(surface, fill_color)
        pygame.draw.polygon(surface, edge_color, self.points, 3)
        self.__surfaces[hash_] = surface
        return surface

    def __flood_fill(self, surface, color):
        bfs = Queue()
        bfs.put_nowait((self.side, self.side))
        visited = set()
        while not bfs.empty():
            point = bfs.get_nowait()
            if (point not in visited) and self.contains_point(point[0], point[1]):
                surface.set_at(point, color)
                visited.add(point)
                bfs.put_nowait((point[0] - 1, point[1]))
                bfs.put_nowait((point[0] + 1, point[1]))
                bfs.put_nowait((point[0], point[1] - 1))
                bfs.put_nowait((point[0], point[1] + 1))

    @staticmethod
    def __calc_hash_of_colors(edge_color: tuple, fill_color: tuple) -> int:
        hash_ = 0
        for i in range(6):
            hash_ <<= 8
            hash_ |= edge_color[i] if i < 3 else fill_color[i - 3]
        return hash_
