from constants import Color
from objects.button import Btn
from objects.player_info import PlayerInfo
from scenes.base import Scene


class MenuScene(Scene):
    def create_objects(self):
        self.button_start = Btn(self.game, (350, 155, 100, 40), Color.WHITE, "Запуск игры", self.set_main_scene)
        self.button_exit = Btn(self.game, (350, 305, 100, 40), Color.WHITE, 'Выход', self.exit)
        self.button_map = Btn(self.game, (350, 205, 100, 40), Color.WHITE, 'Квесты', self.set_quest_scene)
        self.button_quest = Btn(self.game, (350, 255, 100, 40), Color.WHITE, 'Карта мира', self.set_map_scene)
        self.pl_info = PlayerInfo(self.game, lvl="99")
        self.objects = [self.pl_info, self.button_start, self.button_exit, self.button_map, self.button_quest]



    def set_main_scene(self):
        self.set_next_scene(self.game.MAIN_SCENE_INDEX)

    def set_map_scene(self):
        self.set_next_scene(self.game.MAP_SCENE_INDEX)

    def set_quest_scene(self):
        self.set_next_scene(self.game.QUESTS_SCENE_INDEX)

    def exit(self):
        self.game.game_over = True
