from game_eng.player_action import PlayerAction
from net_connection.core_classes import CoreClasses


class ApplyPTPlayerAction(PlayerAction):
    def __init__(self, player, target, pt_set=None):
        super().__init__(player, target)
        self.pt_set = pt_set
        self.pts_type = type(pt_set)

    @staticmethod
    def read_ext(stream, obj, game_model):
        obj.pts_type = CoreClasses.read_class(stream)
        if obj.pts_type in obj.player.pressure_tools:
            obj.pt_set = obj.player.pressure_tools[obj.pts_type]
        else:
            obj.pt_set = None

    @staticmethod
    def write_ext(stream, obj):
        CoreClasses.write_class(stream, obj.pts_type)

    def try_do(self) -> bool:
        success = self.pt_set.try_use(self.target)
        if success and (self.pt_set.count == 0):
            self.player.pressure_tools.pop(type(self.pt_set))
        return success
