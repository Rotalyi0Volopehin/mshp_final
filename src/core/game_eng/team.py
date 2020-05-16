import exceptions


class Team:
    """**Модель фракции**\n
    abstract class\n
    Все наследующие классы должны располагаться в директории 'team_ders'.
    """
    def __init__(self):
        self.game = None
        self.players = []
        self.__current_player_index = 0
        self.money = 0

    @property  # костыль для избежания циклического импорта
    def player_type(self) -> type:
        if not hasattr(Team, "__player_type"):
            from game_eng.player import Player
            Team.__player_type = Player
        return Team.__player_type

    def set_game_model(self, game):
        """**Установка модели игры**\n
        :param game: Модель игры
        :type game: GameModel
        """
        self.game = game

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

    @property
    def money_limit(self) -> int:
        return self.game.teams_money_limit

    def next_player(self):
        """**Передача хода следующему представителю**
        """
        self.__current_player_index += 1
        if self.__current_player_index == len(self.players):
            self.__current_player_index = 0

    def earn_money(self, value: int):
        """**Добавление денег**\n
        Увеличивает значение поля 'money' с учётом лимита бюджета фракций 'money_limit'

        :raises ArgumentTypeException: Неверный тип переданных аргументов
        :param value: Добавляемая денежная сумма
        :type value: int
        """
        if not isinstance(value, int):
            raise exceptions.ArgumentTypeException()
        self.money = min(self.money + value, self.money_limit)
