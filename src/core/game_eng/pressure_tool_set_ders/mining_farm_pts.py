from game_eng.pressure_tool_set import PressureToolSet
from game_eng.grid_tile_effect_ders.mining_farm_effect import MiningFarmGridTileEffect


class MiningFarmPTSet(PressureToolSet):
    __END_PRODUCT__ = None

    @property
    def start_market_count(self) -> int:
        return 5

    @property
    def production_cost(self) -> int:
        return 8

    @property
    def name(self) -> str:
        return "Майнинг Ферма"

    def _try_apply(self, target) -> bool:
        MiningFarmGridTileEffect(target)
        return True
