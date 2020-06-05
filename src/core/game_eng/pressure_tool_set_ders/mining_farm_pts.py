from .effect_giver_pts import EffectGiverPTSet
from game_eng.grid_tile_effect_ders.mining_farm_effect import MiningFarmGridTileEffect


class MiningFarmPTSet(EffectGiverPTSet):
    __END_PRODUCT__ = None
    effect_type = MiningFarmGridTileEffect

    @property
    def start_market_count(self) -> int:
        return 5

    @property
    def production_cost(self) -> int:
        return 8

    @property
    def name(self) -> str:
        return "Майнинг Ферма"
