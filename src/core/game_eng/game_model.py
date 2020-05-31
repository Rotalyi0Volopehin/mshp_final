import exceptions

from game_eng.player_turn import PlayerTurn
from game_eng.market import Market
from game_eng.team import Team
from game_eng.grid_model import GridModel


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
    def __init__(self, title: str, grid_width: int, grid_height: int, player_turn_period: int, teams_money_limit: int):
        # vvv параметры сессии vvv
        if not (isinstance(title, str) and isinstance(player_turn_period, int) and isinstance(teams_money_limit, int)):
            raise exceptions.ArgumentTypeException()
        self.title = title
        self.player_turn_period = player_turn_period
        self.teams_money_limit = teams_money_limit
        # vvv переменные полЯ vvv
        self.grid = GridModel(self, grid_width, grid_height)
        self.teams = list()
        self.market = Market()
        self.__current_team_index = 0
        self.__current_player_turn = self.__current_player = None
        self.__fixed = False

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