import exceptions

from game_eng.grid_tile import GridTile
from game_eng.player import Player


# abstract
class PressureToolSet:
    def __init__(self, player: Player):
        if not isinstance(player, Player):
            raise exceptions.ArgumentTypeException()
        self.count = 0
        self._player = player

    @property  # при наследовании необходимо перегрузить
    def cost(self) -> int:
        raise exceptions.NotImplementedException()

    def try_use(self, target: GridTile) -> bool:
        if not isinstance(target, GridTile):
            raise exceptions.ArgumentTypeException()
        if self.count <= 0:
            return False
        ok = self._try_apply(target)
        if not isinstance(ok, bool):
            raise exceptions.InvalidReturnException()
        if ok:
            self.count -= 1
        return ok

    # vvv при наследовании необходимо перегрузить vvv
    def _try_apply(self, target: GridTile) -> bool:
        raise exceptions.NotImplementedException()
