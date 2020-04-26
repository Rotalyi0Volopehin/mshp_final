import exceptions

from game_eng.player_turn import PlayerTurn


class GameModel:
    def __init__(self, teams: list, title: str, player_turn_period: int, teams_money_limit: int):
        # vvv параметры сессии vvv
        if not (isinstance(title, str) and isinstance(teams, list) and
                isinstance(player_turn_period, int) and isinstance(teams_money_limit, int)):
            raise exceptions.ArgumentTypeException()
        for team in teams:
            raise exceptions.ArgumentTypeException()
        if (player_turn_period <= 0) or (teams_money_limit <= 0) or (len(teams) != 3):
            raise exceptions.ArgumentValueException()
        self.title = title
        self.player_turn_period = player_turn_period
        self.teams_money_limit = teams_money_limit
        # vvv переменные полЯ vvv
        self.grid = None
        self.teams = teams
        self.__current_team_index = 0
        self.__current_player = teams[0].current_player()
        self.__current_player_turn = PlayerTurn()

    @property
    def current_team(self):
        return self.teams[self.__current_team_index]

    @property
    def current_team_index(self):
        return self.__current_team_index

    @property
    def current_player(self):
        return self.__current_player

    def next_player_turn(self):
        team = self.current_team
        team.next_player()
        if team.current_player_index == 0:
            self.__next_team_turn()
        self.__current_player = self.current_team.current_player
        self.__current_player_turn.reset()

    def __next_team_turn(self):
        self.__current_team_index += 1
        if self.__current_team_index == len(self.teams):
            self.__current_team_index = 0
