from constants import Color
from objects.button import Btn
from scenes.base import Scene
from objects.text_bar import TextBar


class GenderScene(Scene):
    def create_objects(self):
        self.button_male = Btn(self.game, (350, 155, 100, 40), Color.WHITE, "Мужчина", self.set_male)
        self.button_female = Btn(self.game, (350, 205, 100, 40), Color.BLUE, "Женщина", self.set_female)

    def set_male(self):
        pass

    def set_female(self):
        pass
