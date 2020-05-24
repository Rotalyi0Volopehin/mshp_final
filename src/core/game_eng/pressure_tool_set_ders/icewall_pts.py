from game_eng.pressure_tool_set import PressureToolSet


class IceWallPTSet(PressureToolSet):
    __END_PRODUCT__ = None

    @property
    def start_market_count(self) -> int:
        return 5

    @property
    def production_cost(self) -> int:
        return 8

    def _try_apply(self, target) -> bool:
        target.gain_power(16)
        return True
