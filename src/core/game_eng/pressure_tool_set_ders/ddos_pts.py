from game_eng.pressure_tool_set_ders.damage_pts import DamagePTSet


class DDosPTSet(DamagePTSet):
    @property
    def cost(self) -> int:
        return 16

    @property
    def damage(self) -> int:
        return 24
