from game_eng.grid_tile import GridTile


class EnhancedGridTile(GridTile):
    @staticmethod
    def get_upgrade_price() -> int:
        return 4

    @property
    def owners_income(self) -> int:
        return 1

    @property
    def power_growth(self) -> int:
        return 2

    @property
    def power_cap(self) -> int:
        return 96

    @property
    def name(self) -> str:
        return "Усиленный Кластер"
