import exceptions

from game_eng.grid_tile_ders.capital_tile import CapitalGridTile
# vvv импорты для чтения/записи vvv
from net_connection.core_classes import CoreClasses
from io_tools.binary_reader import BinaryReader
from io_tools.binary_writer import BinaryWriter


class Team:
    """**Модель фракции**\n
    abstract class\n
    Все наследующие классы должны располагаться в директории 'team_ders'.

    :ivar game: Модель игры
    :vartype game: GameModel
    :ivar players: Игроки
    :vartype players: list
    :ivar money: Бюджет фракции
    :vartype money: int
    :ivar capital_tiles: Контрольные клетки
    :vartype capital_tiles: set
    """
    def __init__(self, game_model):
        if not isinstance(game_model, self.game_model_type):
            raise exceptions.ArgumentTypeException()
        self.game = game_model
        self.__index = len(game_model.teams)
        self.players = []
        self.__current_player_index = 0
        self.money = 0
        self.capital_tiles = set()
        game_model.add_team(self)

    @staticmethod
    def read(stream: BinaryReader, game_model):
        if not isinstance(stream, BinaryReader):
            raise exceptions.ArgumentTypeException()
        team_type = CoreClasses.read_class(stream)
        obj = team_type(game_model)
        obj.__index = stream.read_byte()
        obj.__current_player_index = stream.read_byte()
        obj.money = stream.read_uint()
        tiles = game_model.grid.tiles
        capital_tiles_count = stream.read_byte()
        for _ in range(capital_tiles_count):
            capital_tile_loc_x, capital_tile_loc_y = stream.read_byte_point()
            obj.capital_tiles.add(tiles[capital_tile_loc_x][capital_tile_loc_y])
        return obj

    @staticmethod
    def write(stream: BinaryWriter, obj):
        if not (isinstance(stream, BinaryWriter) and isinstance(obj, Team)):
            raise exceptions.ArgumentTypeException()
        CoreClasses.write_class(stream, type(obj))
        stream.write_byte(obj.__index)
        stream.write_byte(obj.__current_player_index)
        stream.write_uint(obj.money)
        stream.write_byte(len(obj.capital_tiles))
        for capital_tile in obj.capital_tiles:
            capital_tile_loc = (capital_tile.loc_x, capital_tile.loc_y)
            stream.write_byte_point(capital_tile_loc)

    @staticmethod  # костыль для избежания циклического импорта
    def get_player_type() -> type:
        if not hasattr(Team, "__player_type"):
            from game_eng.player import Player
            Team.__player_type = Player
        return Team.__player_type

    @property  # костыль для избежания циклического импорта
    def game_model_type(self) -> type:
        if not hasattr(Team, "__game_model_type"):
            from game_eng.game_model import GameModel
            Team.__game_model_type = GameModel
        return Team.__game_model_type

    @property
    def defeated(self) -> bool:
        """**Факт поражения представителей фракции в этой игровой сессии**\n
        :return: Факт поражения
        :rtype: bool
        """
        return len(self.capital_tiles) == 0

    @property
    def index(self) -> int:
        """**Индекс фракции в списке фракций модели игры**\n
        :return: Индекс фракции
        :rtype: int
        """
        return self.__index

    def add_capital_tile(self, capital_tile: CapitalGridTile):
        """**Добавление контрольной клетки**\n
        :raises ArgumentTypeException: |ArgumentTypeException|
        :param capital_tile: Контрольная клетка
        :type capital_tile: CapitalGridTile
        """
        if not isinstance(capital_tile, CapitalGridTile):
            raise exceptions.ArgumentTypeException()
        self.capital_tiles.add(capital_tile)

    def lose_capital_tile(self, capital_tile: CapitalGridTile):
        """**Утрата контрольной клетки**\n
        :raises ArgumentTypeException: |ArgumentTypeException|
        :raises InvalidOperationException: |InvalidOperationException|
        :param capital_tile: Контрольная клетка
        :type capital_tile: CapitalGridTile
        """
        if not isinstance(capital_tile, CapitalGridTile):
            raise exceptions.ArgumentTypeException()
        if capital_tile not in self.capital_tiles:
            raise exceptions.InvalidOperationException()
        self.capital_tiles.remove(capital_tile)

    def add_player(self, player):
        """**Добавление нового игрока в представители фракции в игровой сессии**\n
        Добавление не должно производиться после начала игры.

        :raises ArgumentTypeException: |ArgumentTypeException|
        :raises ArgumentValueException: |ArgumentValueException|
        :param player: Добавляемый игрок
        :type player: Player
        """
        if not isinstance(player, Team.get_player_type()):
            raise exceptions.ArgumentTypeException()
        if player.team != self:
            raise exceptions.ArgumentValueException()
        self.players.append(player)

    @property
    def name(self) -> str:
        """**Имя фракции**\n
        abstract property

        :raises NotImplementedException: |NotImplementedException|
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

        :raises ArgumentTypeException: |ArgumentTypeException|
        :param value: Добавляемая денежная сумма
        :type value: int
        """
        if not isinstance(value, int):
            raise exceptions.ArgumentTypeException()
        if value > 0:
            self.money = min(self.money + value, self.money_limit)
        else:
            self.money = max(self.money + value, 0)
