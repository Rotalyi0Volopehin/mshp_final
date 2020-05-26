from game_eng.pressure_tool_set import PressureToolSet


class DDosPTSet(PressureToolSet):
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

    def _try_apply(self, target) -> bool:
        if target.power == 0:
            return False
        target.take_damage(24)
        return True
