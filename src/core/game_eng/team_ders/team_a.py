from game_eng.team import Team


class TeamA(Team):
    @property
    def name(self) -> str:
        return "Cyber Corp"
