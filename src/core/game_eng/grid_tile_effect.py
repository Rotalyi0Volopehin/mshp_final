import exceptions

from game_eng.grid_tile import GridTile


class GridTileEffect:
    def __init__(self, tile: GridTile):
        if not isinstance(tile, GridTile):
            raise exceptions.ArgumentTypeException()
        tile.add_effect(self)
        self.tile = tile

    # abstract
    def apply(self):
        pass
