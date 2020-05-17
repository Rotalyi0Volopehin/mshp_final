from game_eng.grid_tile import GridTile


class GridModel:
    def __init__(self, game, width, height):
        self.game = game
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

    def handle_new_team_turn(self):
        for column in self.tiles:
            for tile in column:
                tile.handle_new_team_turn()
