from constants import Color
from objects.button import Btn
from scenes.base import Scene


class QuestScene(Scene):
    def create_objects(self):
        self.button_back = Btn(self.game, (350, 500, 100, 40), Color.WHITE, "Меню", self.game.return_to_upper_scene)
        self.objects = [self.button_back]
