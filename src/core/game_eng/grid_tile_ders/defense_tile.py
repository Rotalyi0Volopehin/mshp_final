from game_eng.grid_tile import GridTile


class DefenseGridTile(GridTile):
    @staticmethod
    def get_upgrade_price() -> int:
        return 16

    @property
    def owners_income(self) -> int:
        return 0

    @property
    def power_growth(self) -> int:
        return 4

    @property
    def power_cap(self) -> int:
        return 128
