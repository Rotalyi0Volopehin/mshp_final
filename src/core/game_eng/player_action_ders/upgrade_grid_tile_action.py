import exceptions

from game_eng.player_action import PlayerAction
from game_eng.grid_tile_upgrade_tree import GridTileUpgradeTree
from net_connection.core_classes import CoreClasses


class UpgradeGridTilePlayerAction(PlayerAction):
    def __init__(self, player, target, upgrade_type=None):
        super().__init__(player, target)
        self.upgrade_type = upgrade_type
        self.__new_tile = None

    @staticmethod
    def read_ext(stream, obj, game_model):
        obj.upgrade_type = CoreClasses.read_class(stream)

    @staticmethod
    def write_ext(stream, obj):
        CoreClasses.write_class(stream, obj.upgrade_type)

    def try_do(self) -> bool:
        if self.target.team != self.player.team:
            raise exceptions.InvalidOperationException()
        try:
            self.__new_tile = GridTileUpgradeTree.upgrade_tile(self.target, self.upgrade_type)
            return True
        except exceptions.InvalidOperationException:
            return False
