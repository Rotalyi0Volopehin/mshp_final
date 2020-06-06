from .effect_giver_pts import EffectGiverPTSet
from game_eng.grid_tile_effect_ders.phishing_effect import PhishingGridTileEffect


class PhishingPTSet(EffectGiverPTSet):
    __END_PRODUCT__ = None
    effect_type = PhishingGridTileEffect

    def create_effect(self, target):
        return self.effect_type(target, self._player.team)

    @property
    def start_market_count(self) -> int:
        return 10

    @property
    def production_cost(self) -> int:
        return 8

    @property
    def name(self) -> str:
        return "Фишинг"
