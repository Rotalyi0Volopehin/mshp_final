from game_eng.grid_tile import GridTile


class EnhancedGridTilePlus(GridTile):
    @staticmethod
    def get_upgrade_price() -> int:
        return 16

    @property
    def owners_income(self) -> int:
        return 2

    @property
    def power_growth(self) -> int:
        return 4

    @property
    def power_cap(self) -> int:
        return 192
