import exceptions

from game_eng.player import Player
from game_eng.grid_tile import GridTile


class PlayerAction:
    """**Модель действия, совершаемого игроком**\n
    abstract class\n
    Этот класс необходим для журналирования ходов.
    """
    def __init__(self, player: Player, target: GridTile):
        if not isinstance(player, Player):
            raise exceptions.ArgumentTypeException()
        self.player = player
        self.target = target

    def try_do(self) -> bool:
        """**Попытка совершить действие**\n
        :raises NotImplementedException: |NotImplementedException|
        :return: ok
        :rtype: bool
        """
        raise exceptions.NotImplementedException()

    def try_undo(self) -> bool:
        """**Попытка отменить действие**\n
        :raises NotImplementedException: |NotImplementedException|
        :return: ok
        :rtype: bool
        """
        raise exceptions.NotImplementedException()
