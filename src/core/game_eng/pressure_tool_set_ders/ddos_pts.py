from game_eng.pressure_tool_set_ders.damage_pts import DamagePTSet


class DDosPTSet(DamagePTSet):
    __END_PRODUCT__ = None

    @property
    def start_market_count(self) -> int:
        return 5

    @property
    def production_cost(self) -> int:
        return 16

    @property
    def name(self) -> str:
        return "DDoS"

    @property
    def damage(self) -> int:
        return 24
