from game_eng.grid_tile_effect import GridTileEffect


class RebootGridTileEffect(GridTileEffect):
    def apply(self):
        self.tile.clear_effects()

    @property
    def name(self) -> str:
        return "Перезагрузка"
