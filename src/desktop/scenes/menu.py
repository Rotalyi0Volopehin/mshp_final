import pygame

from constants import Color
from objects.button import Btn
from scenes.base import Scene
from game_vc.game_vc import GameVC


class MenuScene(Scene):
    def create_objects(self):
        button_exit = Btn(self.game, (350, 305, 100, 40), Color.WHITE, 'Выход', self.game.exit)
        self.objects.append(button_exit)
        button_map = Btn(self.game, (350, 255, 100, 40), Color.WHITE, 'Квесты', self.__set_quest_scene)
        self.objects.append(button_map)
        button_quest = Btn(self.game, (350, 205, 100, 40), Color.WHITE, 'Карта', self.__set_map_scene)
        self.objects.append(button_quest)
        self.game_vc = GameVC(self.game)
        self.objects.append(self.game_vc)

    def __set_map_scene(self):
        from scenes.map import MapScene
        self.game.goto_deeper_scene(MapScene)

    def __set_quest_scene(self):
        from scenes.quests import QuestScene
        self.game.goto_deeper_scene(QuestScene)

    @staticmethod
    def __mute_login_bgm():
        pygame.mixer.music.stop()

    @staticmethod
    def __unmute_login_bgm():
        pygame.mixer.music.play()

    def on_gone_to_deeper_scene_from_this(self):
        MenuScene.__mute_login_bgm()

    def on_returned_to_this_scene(self):
        MenuScene.__unmute_login_bgm()
