import exceptions

from game_eng.pressure_tool_set import PressureToolSet
from game_eng.grid_tile import GridTile


# abstract
class DamagePTSet(PressureToolSet):
    @property
    def damage(self) -> int:
        raise exceptions.NotImplementedException()

    def _try_apply(self, target: GridTile) -> bool:
        dmg = self.damage
        if not isinstance(dmg, int):
            raise exceptions.InvalidReturnException()
        target.power -= dmg
        return True  # да, атаковать можно и себя
