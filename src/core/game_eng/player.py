import exceptions

from game_eng.team import Team


class Player:
    def __init__(self, team: Team):
        if not isinstance(team, Team):
            raise exceptions.ArgumentTypeException()
        self.__team = team

    @property
    def team(self):
        return self.__team
