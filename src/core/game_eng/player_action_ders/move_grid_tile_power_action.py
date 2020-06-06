import exceptions

from game_eng.player_action import PlayerAction


class MoveGridTilePowerPlayerAction(PlayerAction):
    def __init__(self, player, target, selected=None, value=0):
        super().__init__(player, target)
        self.selected = selected
        self.value = value

    @staticmethod
    def read_ext(stream, obj, game_model):
        obj.selected = PlayerAction._read_tile(stream, game_model.grid.tiles)
        obj.value = stream.read_int()

    @staticmethod
    def write_ext(stream, obj):
        PlayerAction._write_tile(stream, obj.selected)
        stream.write_int(obj.value)

    def try_do(self) -> bool:
        if self.selected.team != self.player.team:
            raise exceptions.InvalidOperationException()
        try:
            return self.selected.try_move_power_as_team(self.target, self.value, self.player.team, True)
        except exceptions.ArgumentOutOfRangeException:
            return False
