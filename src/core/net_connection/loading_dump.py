class LoadingDump:
    players = dict()

    @staticmethod
    def add_player(player):
        LoadingDump.players[player.id] = player

    @staticmethod
    def get_player_by_id(uid: int):
        if uid == 0:
            return None
        return LoadingDump.players[uid]

    @staticmethod
    def clear_players():
        LoadingDump.players.clear()

    teams = 3 * [None]

    @staticmethod
    def add_team(team):
        LoadingDump.teams[team.index] = team

    @staticmethod
    def get_team_by_index(team_ind: int):
        if team_ind < 0:
            return None
        return LoadingDump.teams[team_ind]

    game_session = None

    @staticmethod
    def get_current_game_session():
        return LoadingDump.game_session

    @staticmethod
    def set_current_game_session(game_session):
        LoadingDump.game_session = game_session
