from game_eng.pressure_tool_set_ders.damage_pts import DamagePTSet


class DosPTSet(DamagePTSet):
    @property
    def cost(self) -> int:
        return 4

    @property
    def damage(self) -> int:
        return 8
