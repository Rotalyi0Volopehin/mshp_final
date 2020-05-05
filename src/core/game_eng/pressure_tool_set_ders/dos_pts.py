from game_eng.pressure_tool_set_ders.damage_pts import DamagePTSet


class DosPTSet(DamagePTSet):
    __END_PRODUCT__ = None

    @property
    def start_market_count(self) -> int:
        return 10

    @property
    def production_cost(self) -> int:
        return 4

    @property
    def name(self) -> str:
        return "DoS"

    @property
    def damage(self) -> int:
        return 8
