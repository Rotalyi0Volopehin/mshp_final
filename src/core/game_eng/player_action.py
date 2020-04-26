import exceptions

from game_eng.player import Player
from game_eng.grid_tile import GridTile


# abstract
class PlayerAction:
    def __init__(self, player: Player, target: GridTile):
        if not isinstance(player, Player):
            raise exceptions.ArgumentTypeException()
        self.player = player
        self.target = target

    def try_do(self) -> bool:
        raise exceptions.NotImplementedException()

    def try_undo(self) -> bool:
        raise exceptions.NotImplementedException()
