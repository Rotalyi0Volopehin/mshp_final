from game_eng.pressure_tool_set import PressureToolSet
from game_eng.grid_tile_effect_ders.reboot_effect import RebootGridTileEffect


class RebootPTSet(PressureToolSet):
    __END_PRODUCT__ = None

    @property
    def start_market_count(self) -> int:
        return 10

    @property
    def production_cost(self) -> int:
        return 4

    @property
    def name(self) -> str:
        return "Reboot"

    def _try_apply(self, target) -> bool:
        RebootGridTileEffect(target)
        return True
