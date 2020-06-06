import exceptions

from game_eng.player_action import PlayerAction


class MoveGridTilePowerPlayerAction(PlayerAction):
    def __init__(self, player, target, selected=None, value=0):
        if target.team != player.team:
            raise exceptions.InvalidOperationException()
        super().__init__(player, target)
        self.selected = selected
        self.value = value

    @staticmethod
    def read_ext(stream, obj, game_model):
        obj.selected = PlayerAction._read_tile(stream, game_model.grid.tiles)
        obj.value = stream.read_int()

    @staticmethod
    def write_ext(stream, obj):
        stream.write_byte_point(obj.selected)
        stream.write_int(obj.value)

    def try_do(self) -> bool:
        try:
            self.selected.move_power(self.target, self.value)
            return True
        except exceptions.ArgumentOutOfRangeException:
            return False

    def try_undo(self) -> bool:
        try:
            self.target.move_power(self.selected, self.value)
            return True
        except exceptions.ArgumentOutOfRangeException:
            return False
