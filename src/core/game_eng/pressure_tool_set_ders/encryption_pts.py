from game_eng.pressure_tool_set import PressureToolSet


class EncryptionPTSet(PressureToolSet):
    __END_PRODUCT__ = None

    @property
    def start_market_count(self) -> int:
        return 5

    @property
    def production_cost(self) -> int:
        return 8

    @property
    def name(self) -> str:
        return "Шифрование"

    def _try_apply(self, target) -> bool:
        if target.power == target.power_cap:
            return False
        target.gain_power(16)
        return True
