from game_eng.player_action import PlayerAction
from net_connection.core_classes import CoreClasses


class ApplyPTPlayerAction(PlayerAction):
    def __init__(self, player, target, pt_set=None):
        super().__init__(player, target)
        self.pt_set = pt_set

    @staticmethod
    def read_ext(stream, obj, game_model):
        pts_type = CoreClasses.read_class(stream)
        obj.pt_set = obj._player.pressure_tools[pts_type]

    @staticmethod
    def write_ext(stream, obj):
        CoreClasses.write_class(stream, type(obj.pt_set))

    def try_do(self) -> bool:
        return self.pt_set.try_use(self.target)
