import time

from game_eng.game_model import GameModel
from game_eng.team_ders.team_a import TeamA
from game_eng.team_ders.team_b import TeamB
from game_eng.team_ders.team_c import TeamC
from game_eng.player import Player
from game_vc.grid_controller import GridTileController
from game_eng.grid_model import GridModel
from game_vc.grid_view import GridTileView
from scenes.base import Scene
from constants import Color
# vvv импорт компонентов формы vvv
from objects.button import Btn


class GameVC(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.__turn_start_time = time.time()

    def create_objects(self):
        self.__create_logic_objects()
        self.__create_form_objects()
        self.__link_logic_and_form_objects()

    def __create_logic_objects(self):
        teams = [TeamA(), TeamB(), TeamC()]
        for i in range(len(teams)):
            team = teams[i]
            team.add_player(Player(f"P{i}A", team))
            team.add_player(Player(f"P{i}B", team))
        self.model = GameModel(teams, title="Hardcoded session", player_turn_period=30, teams_money_limit=999)
        # vvv страшный код vvv
        grid_model = GridModel(self.game)
        self.grid_controller = GridTileController(grid_model)
        self.grid_view = GridTileView(self.game, grid_model, self.grid_controller)
        self.grid_controller.init_view(self.grid_view)

    def __create_form_objects(self):
        self.button_back = Btn(self.game, (350, 500, 100, 40), Color.WHITE, 'Меню', self.__back_to_menu)

    def __link_logic_and_form_objects(self):
        pass

    def __back_to_menu(self):
        from scenes.menu import MenuScene
        self.game.change_scene(MenuScene)

    def process_all_logic(self):
        if time.time() - self.__turn_start_time >= self.model.player_turn_period:
            self.__next_turn()  # TODO: переписать для сетевой игры (потребуется асинхронная синхронизация)
            self.__turn_start_time = time.time()

    def __next_turn(self):
        self.model.next_player_turn()
