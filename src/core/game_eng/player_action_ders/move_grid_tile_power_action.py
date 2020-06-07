import exceptions

from game_eng.player_action import PlayerAction


class MoveGridTilePowerPlayerAction(PlayerAction):
    def __init__(self, player, target, selected=None, value=0):
        super().__init__(player, target)
        self.selected = selected
        self.value = value

    @staticmethod
    def read_ext(stream, obj, game_model):
        selected_loc = stream.read_byte_point()
        obj.selected = game_model.grid.tiles[selected_loc[0]][selected_loc[1]]
        obj.value = stream.read_int()

    @staticmethod
    def write_ext(stream, obj):
        stream.write_byte_point((obj.selected.loc_x, obj.selected.loc_y))
        stream.write_int(obj.value)

    def try_do(self) -> bool:
        if self.selected.team != self.player.team:
            raise exceptions.InvalidOperationException()
        try:
            return self.selected.try_move_power_as_team(self.target, self.value, self.player.team, True)
        except exceptions.ArgumentOutOfRangeException:
            return False
