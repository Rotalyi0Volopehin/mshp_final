from game_eng.team import Team


class TeamB(Team):
    @property
    def name(self) -> str:
        return "Добрая Воля"
