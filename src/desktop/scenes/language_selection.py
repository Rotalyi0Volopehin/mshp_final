import os
from constants import Color
from objects.button import Btn
from scenes.base import Scene
from scenes.stats import StatsMenuScene


class LanguageScene(Scene):

    def create_objects(self):
        self.language_path = os.path.join('quests', 'language')
        self.button_spanish = Btn(self.game, (350, 105, 100, 40), Color.WHITE, "Español", self.set_spanish)
        self.button_russian = Btn(self.game, (350, 155, 100, 40), Color.WHITE, 'Русский', self.set_russian)
        self.button_english = Btn(self.game, (350, 205, 100, 40), Color.WHITE, 'English', self.set_english)
        self.button_german = Btn(self.game, (350, 255, 100, 40), Color.WHITE, 'Deutsch', self.set_german)
        self.button_french = Btn(self.game, (350, 305, 100, 40), Color.WHITE, 'Français', self.set_french)
        self.button_exit = Btn(self.game, (350, 405, 100, 40), Color.WHITE, 'Выход', self.exit)
        self.objects = [self.button_spanish, self.button_exit,  self.button_russian,
                        self.button_english, self.button_german, self.button_french]

    def set_spanish(self):
        file = open(self.language_path, 'w')
        file.write('es')
        file.close()
        self.game.set_origin_scene(StatsMenuScene)

    def set_russian(self):
        file = open(self.language_path, 'w')
        file.write('ru')
        file.close()
        self.game.set_origin_scene(StatsMenuScene)

    def set_english(self):
        file = open(self.language_path, 'w')
        file.write('en')
        file.close()
        self.game.set_origin_scene(StatsMenuScene)

    def set_german(self):
        file = open(self.language_path, 'w')
        file.write('de')
        file.close()
        self.game.set_origin_scene(StatsMenuScene)

    def set_french(self):
        file = open(self.language_path, 'w')
        file.write('fr')
        file.close()
        self.game.set_origin_scene(StatsMenuScene)

    def exit(self):
        self.game.game_over = True