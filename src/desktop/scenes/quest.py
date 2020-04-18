from constants import Color
from objects.button import Btn
from objects.text_bar import TextBar
from objects.text import Text
from objects.image import Image
from scenes.base import Scene


class QuestScene(Scene):

    def create_objects(self):
        self.text_bar = TextBar(self.game, file_name='text_0', path_to_file='quests/quest_1/', func=self.back_to_menu)
        self.image_char = Image(self.game, file_name='images/cyber.png', x=100, y=300)
        self.button_back = Btn(self.game, (350, 500, 100, 40), Color.WHITE, "Меню", self.back_to_menu)
        self.objects = [self.button_back, self.image_char, self.text_bar]


    def back_to_menu(self):
        self.set_next_scene(self.game.MENU_SCENE_INDEX)