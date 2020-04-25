from constants import Color
from objects.button import Btn
from objects.image import Image
from scenes.base import Scene


class QuestScene(Scene):
    def create_objects(self):
        self.image_bg = Image(self.game, file_name='images/Background.png', x=0, y=0)
        self.button_back = Btn(self.game, (350, 500, 100, 40), Color.WHITE, "Меню", self.back_to_menu)
        self.objects = [self.image_bg, self.button_back]

    def back_to_menu(self):
        self.set_next_scene(self.game.MENU_SCENE_INDEX)
