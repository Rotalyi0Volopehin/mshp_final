import exceptions


class Team:
    """**Модель фракции**\n
    abstract class\n
    Все наследующие классы должны располагаться в директории 'team_ders'.
    """
    def __init__(self):
        self.players = []
        self.__current_player_index = 0
        self.money = 0

    @property  # костыль для избежания циклического импорта
    def player_type(self) -> type:
        if not hasattr(Team, "__player_type"):
            from game_eng.player import Player
            Team.__player_type = Player
        return Team.__player_type

    def add_player(self, player):
        """**Добавление нового игрока в представители фракции в игровой сессии**\n
        Добавление не должно производиться после начала игры.

        :raises ArgumentTypeException: Неверный тип переданных аргументов
        :raises ArgumentValueException: Значение переданных аргументов не соответсвует требованиям
        :param player: Добавляемый игрок
        :type player: Player
        """
        if not isinstance(player, self.player_type):
            raise exceptions.ArgumentTypeException()
        if player.team != self:
            raise exceptions.ArgumentValueException()
        self.players.append(player)

    @property
    def name(self) -> str:
        """**Имя фракции**\n
        abstract property

        :raises NotImplementedException: Нет реализации
        :return: Имя
        :rtype: str
        """
        raise exceptions.NotImplementedException()

    @property
    def current_player(self):
        """**Игрок, делающий ход, если сейчас ход этой фракции**\n
        :return: Представитель под номером 'current_player_index'
        :rtype: Player
        """
        return self.players[self.__current_player_index]

    @property
    def current_player_index(self) -> int:
        """**Номер представителя, делающего ход, если сейчас ход этой фракции**\n
        :return: Номер представителя
        :rtype: int
        """
        return self.__current_player_index

    def next_player(self):
        """**Передача хода следующему представителю**
        """
        self.__current_player_index += 1
        if self.__current_player_index == len(self.players):
            self.__current_player_index = 0
