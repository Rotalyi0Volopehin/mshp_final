from game_eng.pressure_tool_set import PressureToolSet


class EffectGiverPTSet(PressureToolSet):
    effect_type = None

    def create_effect(self, target):
        return self.effect_type(target)

    def _try_apply(self, target) -> bool:
        if target.has_effect(self.effect_type):
            return False
        self.create_effect(target)
        return True
