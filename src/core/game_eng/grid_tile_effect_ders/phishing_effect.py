from game_eng.grid_tile_effect import GridTileEffect


class PhishingGridTileEffect(GridTileEffect):
    def __init__(self, tile, team):
        super().__init__(tile)
        self.team = team

    def apply(self):
        self.tile.remove_effect(self)
        self.team.earn_money(self.tile.owners_income)
        if self.tile.team is not None:
            self.tile.team.earn_money(-self.tile.owners_income)
