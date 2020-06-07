from game_eng.grid_tile_effect import GridTileEffect
from .virus_effect import VirusGridTileEffect


class AntivirusGridTileEffect(GridTileEffect):
    def apply(self):
        self.tile.gain_power(1)
        self.tile.try_remove_effect_with_type(VirusGridTileEffect)

    @property
    def name(self) -> str:
        return "Антивирус"
