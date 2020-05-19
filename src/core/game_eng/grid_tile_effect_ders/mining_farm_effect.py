from game_eng.grid_tile_effect import GridTileEffect


class MiningFarmGridTileEffect(GridTileEffect):
    def apply(self):
        if self.tile.team is not None:
            self.tile.team.earn_money(self.tile.owners_income)

    @property
    def name(self) -> str:
        return "Майнинг Ферма"
