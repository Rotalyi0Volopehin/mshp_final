from constants import Color
from objects.button import Btn
from objects.text import Text
from scenes.base import Scene
from game_vc.game_vc import GameVC


class GSMenuScene(Scene):
    def __init__(self, game, gs=None):
        self.gs = gs
        self.game_vc = None
        super().__init__(game)

    def create_objects(self):
        text_game = Text(self.game, font_size=45, is_bold=True, text='NetWar',
                         color=Color.WHITE, x=400, y=100)
        self.objects.append(text_game)
        text_game = Text(self.game, font_size=45, is_bold=True, text='Игрок: '+self.game.username,
                         color=Color.WHITE, x=400, y=150)
        self.objects.append(text_game)
        button_exit = Btn(self.game, (550, 510, 200, 40), text='Выход', function=self.game.exit)
        self.objects.append(button_exit)
        button_exit = Btn(self.game, (50, 510, 200, 40), text='Выход из аккаунта',
                          function=self.__set_login_menu)
        self.objects.append(button_exit)
        button_map = Btn(self.game, (300, 255, 200, 40), text='Квесты',
                         function=self.__set_quest_scene)
        self.objects.append(button_map)
        button_quest = Btn(self.game, (300, 205, 200, 40), text='Активная сессия',
                           function=self.__set_map_scene)
        self.objects.append(button_quest)
        self.game_vc = GameVC(self.game, game_model=self.gs)
        self.objects.append(self.game_vc)

    def __set_map_scene(self):
        from scenes.map import MapScene
        self.game.goto_deeper_scene(MapScene)

    def __set_quest_scene(self):
        from scenes.quests import QuestScene
        self.game.goto_deeper_scene(QuestScene)

    def __set_login_menu(self):
        from scenes.login import LoginScene
        self.game.username = ''
        self.game.set_origin_scene(LoginScene)
