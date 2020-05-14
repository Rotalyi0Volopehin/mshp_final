from game_eng.grid_tile import GridTile


# noinspection PyRedundantParentheses
class GridModel:
    def __init__(self, width, height):
        self.height = height
        self.width = width
        self.tiles = None
        self.__create_tiles()
        self.controller = self.view = None

    def __create_tiles(self):
        self.tiles = []
        for ix in range(self.width):
            column = []
            for iy in range(self.height):
                tile = GridTile(self, ix, iy)
                column.append(tile)
            self.tiles.append(column)

    def set_view(self, view):
        self.view = view

    def set_controller(self, controller):
        self.controller = controller

    # TODO: вынести абилки в отдельные классы

    @staticmethod
    def ability_emp(target):
        for neighbour in target.get_neighbours():
            neighbour.power = max(neighbour.power - 16, 0)

    @staticmethod
    def ability_fishing(target):
        target.power = max(target.power - 32, 0)
