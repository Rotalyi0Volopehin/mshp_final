import exceptions

from game_eng.pressure_tool_set import PressureToolSet


class EffectGiverPTSet(PressureToolSet):
    effect_type = None

    def create_effect(self, target):
        return self.effect_type(target)

    def _try_apply(self, target) -> bool:
        if target.has_effect(self.effect_type):
            return False
        self.__effect = self.create_effect(target)
        self.__target = target
        return True

    def try_cancel(self) -> bool:
        if not hasattr(self, "__target"):
            raise exceptions.InvalidOperationException()
        self.__target.remove_effect(self.__effect)
        del self.__target
        del self.__effect
        return True
