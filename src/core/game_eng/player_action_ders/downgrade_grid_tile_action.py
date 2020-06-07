import exceptions

from game_eng.player_action import PlayerAction
from game_eng.grid_tile_upgrade_tree import GridTileUpgradeTree


class DowngradeGridTilePlayerAction(PlayerAction):
    def __init__(self, player, target):
        super().__init__(player, target)
        self.__upgrade_type = self.__new_tile = None

    def try_do(self) -> bool:
        if self.target.team != self.player.team:
            raise exceptions.InvalidOperationException()
        try:
            self.__upgrade_type = type(self.target)
            self.__new_tile = GridTileUpgradeTree.downgrade_tile(self.target)
            return True
        except exceptions.InvalidOperationException:
            return False
