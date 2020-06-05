import exceptions

from game_eng.grid_tile import GridTile
from game_eng.grid_tile_ders.enhanced_tile import EnhancedGridTile
from game_eng.grid_tile_ders.defense_tile import DefenseGridTile
from game_eng.grid_tile_ders.service_tile import ServiceGridTile
from game_eng.grid_tile_ders.enhanced_tile_plus import EnhancedGridTilePlus
from game_eng.grid_tile_ders.defense_tile_plus import DefenseGridTilePlus
from game_eng.grid_tile_ders.service_tile_plus import ServiceGridTilePlus
from game_eng.grid_tile_ders.capital_tile import CapitalGridTile


class GridTileUpgradeTree:
    tile_upgrade_bases = {
        GridTile: None,
        CapitalGridTile: None,
        EnhancedGridTile: GridTile,
        DefenseGridTile: EnhancedGridTile,
        ServiceGridTile: EnhancedGridTile,
        EnhancedGridTilePlus: EnhancedGridTile,
        DefenseGridTilePlus: DefenseGridTile,
        ServiceGridTilePlus: ServiceGridTile,
    }

    @staticmethod
    def get_available_upgrades_for_tile_type(tile_type: type) -> set:
        if not isinstance(tile_type, type):
            raise exceptions.ArgumentTypeException()
        if not issubclass(tile_type, GridTile):
            raise exceptions.ArgumentValueException()
        upgrades = set()
        for tile_type_, base_type in GridTileUpgradeTree.tile_upgrade_bases:
            if base_type == tile_type:
                upgrades.add(tile_type_)
        return upgrades

    @staticmethod
    def upgrade_tile(tile: GridTile, upgrade: type) -> GridTile:
        if not (isinstance(tile, GridTile) and isinstance(upgrade, type)):
            raise exceptions.ArgumentTypeException()
        if not issubclass(upgrade, GridTile):
            raise exceptions.ArgumentValueException()
        if (tile.team is None) or (tile.team.money < upgrade.get_upgrade_price()) or \
                (GridTileUpgradeTree.tile_upgrade_bases[upgrade] != type(tile)):
            raise exceptions.InvalidOperationException()
        tile.team.money -= upgrade.get_upgrade_price()
        return tile.upgrade(upgrade)

    @staticmethod
    def downgrade_tile(tile: GridTile, cashback: bool = False) -> GridTile:
        if not isinstance(tile, GridTile):
            raise exceptions.ArgumentTypeException()
        base = GridTileUpgradeTree.tile_upgrade_bases[type(tile)]
        if base is None:
            raise exceptions.InvalidOperationException()
        if cashback:
            tile.team.earn_money(tile.get_upgrade_price())
        return tile.upgrade(base)
