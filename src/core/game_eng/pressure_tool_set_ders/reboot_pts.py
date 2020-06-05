from .effect_giver_pts import EffectGiverPTSet
from game_eng.grid_tile_effect_ders.reboot_effect import RebootGridTileEffect


class RebootPTSet(EffectGiverPTSet):
    __END_PRODUCT__ = None
    effect_type = RebootGridTileEffect

    @property
    def start_market_count(self) -> int:
        return 10

    @property
    def production_cost(self) -> int:
        return 4

    @property
    def name(self) -> str:
        return "Перезагрузка"
