from objects.button import Btn
from scenes.base import Scene
from game_vc.game_vc import GameVC


class GSMenuScene(Scene):
    def create_objects(self):
        button_exit = Btn(self.game, (350, 305, 100, 40), text='Выход', function=self.game.exit)
        self.objects.append(button_exit)
        button_map = Btn(self.game, (350, 255, 100, 40), text='Квесты', function=self.__set_quest_scene)
        self.objects.append(button_map)
        button_quest = Btn(self.game, (350, 205, 100, 40), text='Карта', function=self.__set_map_scene)
        self.objects.append(button_quest)
        self.game_vc = GameVC(self.game)
        self.objects.append(self.game_vc)

    def __set_map_scene(self):
        from scenes.map import MapScene
        self.game.goto_deeper_scene(MapScene)

    def __set_quest_scene(self):
        from scenes.quests import QuestScene
        self.game.goto_deeper_scene(QuestScene)
