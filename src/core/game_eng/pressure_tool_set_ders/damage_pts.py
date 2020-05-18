import exceptions

from game_eng.pressure_tool_set import PressureToolSet


# abstract
class DamagePTSet(PressureToolSet):
    @property
    def damage(self) -> int:
        raise exceptions.NotImplementedException()

    def _try_apply(self, target) -> bool:
        dmg = self.damage
        if not isinstance(dmg, int):
            raise exceptions.InvalidReturnException()
        target.take_damage(dmg)
        return True  # да, атаковать можно и себя
