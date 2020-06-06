import exceptions

from game_eng.player_action import PlayerAction
# vvv импорты для чтения/записи vvv
from io_tools.binary_reader import BinaryReader
from io_tools.binary_writer import BinaryWriter


class PlayerTurn:
    """**Данные о ходе игрока**\n
    Этот класс необходим для журналирования ходов.
    """
    def __init__(self):
        self.actions = []

    @staticmethod
    def read(stream: BinaryReader, game_model):
        if not isinstance(stream, BinaryReader):
            raise exceptions.ArgumentTypeException()
        obj = PlayerTurn()
        obj.actions = stream.read_iterable(PlayerAction, {"game_model": game_model})
        return obj

    @staticmethod
    def write(stream: BinaryWriter, obj):
        if not (isinstance(stream, BinaryWriter) and isinstance(obj, PlayerTurn)):
            raise exceptions.ArgumentTypeException()
        stream.write_iterable(obj.actions, PlayerAction)

    def try_act(self, action: PlayerAction) -> bool:
        """**Попытка совершения действия**\n
        Пробует выполнить действие. Добавляет в стэк, если удачно.

        :raises ArgumentTypeException: |ArgumentTypeException|
        :param action: Действие
        :type action: PlayerAction
        :return: ok
        :rtype: bool
        """
        if not isinstance(action, PlayerAction):
            raise exceptions.ArgumentTypeException()
        if action.try_do():
            self.actions.append(action)
            return True
        return False

    def try_undo(self) -> bool:
        """**Попытка отмены действия**\n
        Пробует отменить последнее действие. Убирает его из стэка, если удачно.

        :return: ok
        :rtype: bool
        """
        if len(self.actions) == 0:
            return False
        action = self.actions[-1]
        if action.try_undo():
            self.actions.pop(-1)
            return True
        return False

    def sync(self):
        """**Выполняет все действия стэка**\n
        Используется для синхронизации игрового состояния у всех игроков.
        """
        for action in self.actions:
            if not action.try_do():
                raise exceptions.InvalidOperationException(f"Sync failed on execution of '{type(action)}'!")
