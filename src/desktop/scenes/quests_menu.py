from constants import Color
from objects.button import Btn
from scenes.base import Scene


class QuestMenuScene(Scene):
    def create_objects(self):
        self.quest_1 = Btn(self.game, (100, 100, 100, 40), Color.WHITE, "Квест 1", self.set_quest_1)
        self.quest_2 = Btn(self.game, (350, 500, 100, 40), Color.WHITE, "Квест 2", self.set_quest_1)
        self.quest_3 = Btn(self.game, (350, 500, 100, 40), Color.WHITE, "Квест 3", self.set_quest_1)
        self.quest_4 = Btn(self.game, (350, 500, 100, 40), Color.WHITE, "Квест 4", self.set_quest_1)
        self.button_back = Btn(self.game, (350, 500, 100, 40), Color.WHITE, "Меню", self.back_to_menu)

        self.objects = [self.button_back, self.quest_1]

    def back_to_menu(self):
        self.set_next_scene(self.game.MENU_SCENE_INDEX)

    def set_quest_1(self):
        self.set_next_scene(self.game.QUEST_SCENE_INDEX)

    def set_quest_2(self):
        pass

    def set_quest_3(self):
        pass

    def set_quest_4(self):
        pass
