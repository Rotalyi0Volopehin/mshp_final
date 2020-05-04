import exceptions


# abstract
class Team:
    def __init__(self):
        self.players = []
        self.__current_player_index = 0
        self.money = 0

    @property
    def player_type(self):
        if not hasattr(Team, "__player_type"):
            from game_eng.player import Player
            Team.__player_type = Player
        return Team.__player_type

    def add_player(self, player):
        if not isinstance(player, self.player_type):
            raise exceptions.ArgumentTypeException()
        if player.team != self:
            raise exceptions.ArgumentValueException()
        self.players.append(player)

    @property
    def name(self) -> str:
        raise exceptions.NotImplementedException()

    @property
    def current_player(self):
        return self.players[self.__current_player_index]

    @property
    def current_player_index(self):
        return self.__current_player_index

    def next_player(self):
        self.__current_player_index += 1
        if self.__current_player_index == len(self.players):
            self.__current_player_index = 0
