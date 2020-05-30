from game_eng.grid_tile_effect import GridTileEffect


class VirusGridTileEffect(GridTileEffect):
    def apply(self):
        if self.tile.power > 0:
            self.tile.power -= 1
        else:
            for neighbour in self.tile.get_neighbours():
                if neighbour.has_effect(VirusGridTileEffect):
                    continue
                VirusGridTileEffect(neighbour)

    @property
    def name(self) -> str:
        return "Вирус"
