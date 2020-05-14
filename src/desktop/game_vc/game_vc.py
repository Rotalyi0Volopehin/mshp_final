import time

from game_eng.game_model import GameModel
from game_eng.team_ders.team_a import TeamA
from game_eng.team_ders.team_b import TeamB
from game_eng.team_ders.team_c import TeamC
from game_eng.player import Player
from game_eng.grid_model import GridModel
from game_vc.grid_vc import GridVC
from objects.base import DrawObject


class GameVC(DrawObject):
    def __init__(self, game):
        super().__init__(game)
        self.__turn_start_time = time.time()
        self.model = create_hardcoded_game_model()
        self.grid = GridModel(6, 6)
        self.grid_vc = GridVC(self.grid, self.game)

    def process_logic(self):
        self.grid_vc.process_logic()
        if time.time() - self.__turn_start_time >= self.model.player_turn_period:
            self.__next_turn()  # TODO: переписать для сетевой игры (потребуется асинхронная синхронизация)
            self.__turn_start_time = time.time()

    def process_event(self, event):
        scene = type(self.game.current_scene).__name__
        if scene.startswith("Map"):
            self.grid_vc.process_event(event)

    def process_draw(self):
        scene = type(self.game.current_scene).__name__
        if scene.startswith("Map"):
            self.grid_vc.process_draw()

    def __next_turn(self):
        self.model.next_player_turn()


def create_hardcoded_game_model() -> GameModel:
    teams = [TeamA(), TeamB(), TeamC()]
    for i in range(len(teams)):
        team = teams[i]
        player = Player(f"P{i}A", team)
        team.add_player(player)
        team.add_player(Player(f"P{i}B", team))
        return GameModel(teams, title="Hardcoded session", player_turn_period=30, teams_money_limit=999)
