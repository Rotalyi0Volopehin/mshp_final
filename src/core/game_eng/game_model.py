import exceptions

from game_eng.player_turn import PlayerTurn
from game_eng.market import Market
from game_eng.team import Team
from game_eng.grid_model import GridModel
from game_eng.player import Player
from game_eng.pressure_tool_set import PressureToolSet
# vvv импорты для чтения/записи vvv
from net_connection.loading_dump import LoadingDump
from io_tools.binary_reader import BinaryReader
from io_tools.binary_writer import BinaryWriter


class GameModel:
    """**Модель игры**\n
    :ivar title: Название игровой сессии
    :vartype title: str
    :ivar player_turn_period: Максимальная продолжительность хода любого игрока
    :vartype player_turn_period: int
    :ivar teams_money_limit: Лимит бюджета фракций
    :vartype teams_money_limit: int
    :ivar grid: Модель сетки
    :vartype grid: GridModel
    :ivar teams: Список фракций
    :vartype teams: list
    :ivar market: Локальный Даркнет сессии
    :vartype market: Market
    """
    def __init__(self, title: str, player_turn_period: int, teams_money_limit: int,
                 grid_width: int, grid_height: int, stream: BinaryReader = None):
        # vvv параметры сессии vvv
        if not (isinstance(title, str) and isinstance(player_turn_period, int) and isinstance(teams_money_limit, int)
                and isinstance(grid_width, int) and isinstance(grid_height, int) and
                (isinstance(stream, BinaryReader) or (stream is None))):
            raise exceptions.ArgumentTypeException()
        self.title = title
        self.player_turn_period = player_turn_period
        self.teams_money_limit = teams_money_limit
        # vvv переменные полЯ vvv
        self.__current_team_index = 0
        self.__current_player_turn = self.__current_player = None
        self.__fixed = False
        self.teams = list()
        if stream is None:
            self.grid = GridModel(self, grid_width, grid_height)
            self.market = Market()
        else:
            LoadingDump.set_current_game_session(self)
            self.grid = GridModel.read(stream)
            self.market = Market.read(stream)
            for _ in range(3):
                Team.read(stream)
            stream.read_iterable(PlayerTurn)
            stream.read_iterable(PressureToolSet)

    @staticmethod
    def read(stream: BinaryReader):
        if not isinstance(stream, BinaryReader):
            raise exceptions.ArgumentTypeException()
        title = stream.read_short_string()
        player_turn_period = stream.read_byte()
        teams_money_limit = stream.read_uint()
        obj = GameModel(title, player_turn_period, teams_money_limit, 0, 0, stream)
        return obj

    @staticmethod
    def write(stream: BinaryWriter, obj):
        if not (isinstance(stream, BinaryWriter) and isinstance(obj, GameModel)):
            raise exceptions.ArgumentTypeException()
        pass  # TODO: дописать запись игровой сессии

    def start_game(self):
        """**Окончание инициализации**\n
        Запрещает запуск метода add_team.
        """
        self.__fixed = True
        self.__current_player = self.current_team.current_player
        self.__current_player_turn = PlayerTurn()
        self.grid.handle_new_team_turn()

    def add_team(self, team: Team):
        """**Добавление фракции**\n
        Добавлять необходимо до начала игры.
        Максимальное число - 3.

        :raises ArgumentTypeException: |ArgumentTypeException|
        :raises InvalidOperationException: |InvalidOperationException|
        :param team: Фракция
        :type team: Team
        """
        if not isinstance(team, Team):
            raise exceptions.ArgumentTypeException()
        if (len(self.teams) >= 3) or self.__fixed:
            raise exceptions.InvalidOperationException()
        self.teams.append(team)

    @property
    def current_team(self) -> Team:
        """**Фракция, игроки которой сейчас ходят**\n
        :return: Фракция под номером 'current_team_index'
        :rtype: Team
        """
        return self.teams[self.__current_team_index]

    @property
    def current_team_index(self) -> int:
        """**Номер фракции, игроки которой сейчас ходят**\n
        :return: Номер фракции
        :rtype: int
        """
        return self.__current_team_index

    @property
    def current_player(self):
        """**Игрок, совершающий ход**\n
        :return: Игрок
        :rtype: Player
        """
        return self.__current_player

    def next_player_turn(self):
        """**Передача хода следующему игроку**\n
        Если следующий игрок пренадлежит другой фракции, производится передача хода его фракции.
        """
        team = self.current_team
        team.next_player()
        if team.current_player_index == 0:
            self.__next_team_turn()
        self.__current_player = self.current_team.current_player
        self.__current_player_turn.reset()

    def find_player_by_name(self, name: str):
        if not isinstance(name, str):
            raise exceptions.ArgumentTypeException()
        for team in self.teams:
            player = team.find_player_by_name(name)
            if player is not None:
                return player
        return None

    def __next_team_turn(self):
        self.market.update()
        self.__current_team_index += 1
        if self.__current_team_index == len(self.teams):
            self.__current_team_index = 0
        self.grid.handle_new_team_turn()
