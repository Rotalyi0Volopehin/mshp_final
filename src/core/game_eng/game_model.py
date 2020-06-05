import exceptions

from datetime import datetime
from game_eng.player_turn import PlayerTurn
from game_eng.market import Market
from game_eng.team import Team
from game_eng.grid_model import GridModel
from game_eng.player import Player
# vvv импорты для чтения/записи vvv
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
        self.player_ids = dict()
        if stream is None:
            self.grid = GridModel(self, grid_width, grid_height)
            self.market = Market()
            self.turn_beginning_time = datetime.utcnow()
        else:
            self.turn_beginning_time = stream.read_datetime()
            self.grid = GridModel.read(stream, self)
            self.market = Market.read(stream)
            for _ in range(3):
                Team.read(stream, self)
            stream.read_short_iterable(Player, {"game_model": self})
            self.start_game()

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
        stream.write_short_string(obj.title)
        stream.write_byte(obj.player_turn_period)
        stream.write_uint(obj.teams_money_limit)
        stream.write_datetime(obj.turn_beginning_time)
        GridModel.write(stream, obj.grid)
        Market.write(stream, obj.market)
        for team in obj.teams:
            Team.write(stream, team)
        stream.write_short_iterable(obj.player_ids.values(), Player)

    def start_game(self):
        """**Окончание инициализации**\n
        Запрещает запуск метода add_team.
        """
        for team in self.teams:
            for player in team.players:
                self.player_ids[player.id] = player
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
    def turn_time_elapsed(self) -> float:
        return datetime.utcnow().timestamp() - self.turn_beginning_time.timestamp()

    @property
    def turn_time_left(self) -> float:
        return self.player_turn_period - self.turn_time_elapsed

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
        self.turn_beginning_time = datetime.utcnow()

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
        print(self.current_team_index, len(self.teams), self.current_team.defeated)
        self.__current_team_index += 1
        self.__current_team_index = self.__current_team_index % len(self.teams)
        while self.current_team.defeated:
            self.__current_team_index += 1
            self.__current_team_index = self.__current_team_index % len(self.teams)
        flag = self.check_winner()
        if flag:
            pass
            #self.grid.game.return_to_upper_scene()
        self.grid.handle_new_team_turn()

    def check_winner(self):
        lose_count = 0
        winner = 0
        for i in self.teams:
            if i.defeated:
                lose_count += 1
            else:
                winner = i
        if lose_count >= 2:
            print("WINNER: ", winner)
        return True

def create_new_game_model(title: str, player_turn_period: int, teams_money_limit: int, players_data) -> GameModel:
    game = GameModel(title, player_turn_period, teams_money_limit, 11, 11)
    from game_eng.team_ders.team_a import TeamA
    from game_eng.team_ders.team_b import TeamB
    from game_eng.team_ders.team_c import TeamC
    for team_type in (TeamA, TeamB, TeamC):
        team_type(game)
    for player_data in players_data:
        team = game.teams[player_data["team"]]
        Player(player_data["uid"], player_data["name"], team)
    from game_eng.grid_tile_ders.capital_tile import CapitalGridTile
    tiles = game.grid.tiles

    def make_capital_tile(x, y, team):
        tile = tiles[x][y]
        tile = tile.upgrade(CapitalGridTile)
        tile.team = team
    make_capital_tile(1, 5, game.teams[0])
    make_capital_tile(7, 1, game.teams[1])
    make_capital_tile(7, 9, game.teams[2])
    make_capital_tile(5, 5, None)
    game.start_game()
    empty_tiles = [(0, 0), (1, 0), (2, 0), (9, 0), (10, 0), (0, 1), (1, 1), (3, 1), (9, 1), (10, 1), (0, 2), (1, 2),
                   (4, 2), (10, 2), (0, 3), (6, 3), (10, 3), (0, 4), (5, 4), (3, 5), (6, 5), (8, 5), (9, 5), (0, 6),
                   (5, 6), (0, 7), (6, 7), (10, 7), (0, 8), (1, 8), (4, 8), (10, 8), (0, 9), (1, 9), (3, 9), (9, 9),
                   (10, 9), (0, 10), (1, 10), (2, 10), (9, 10), (10, 10)]
    for empty_tile in empty_tiles:
        x = empty_tile[0]
        y = empty_tile[1]
        tiles[x][y] = None
    return game
