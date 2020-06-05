from game_eng.pressure_tool_set import PressureToolSet
from game_eng.grid_tile_effect_ders.phishing_effect import PhishingGridTileEffect


class PhishingPTSet(PressureToolSet):
    __END_PRODUCT__ = None

    @property
    def start_market_count(self) -> int:
        return 10

    @property
    def production_cost(self) -> int:
        return 8

    @property
    def name(self) -> str:
        return "Фишинг"

    def _try_apply(self, target) -> bool:
        PhishingGridTileEffect(target, self._player.team)
        return True
