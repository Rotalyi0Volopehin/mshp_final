from constants import Color
from objects.button import Btn
from scenes.base import Scene


class LanguageScene(Scene):

    def create_objects(self):
        self.button_spanish = Btn(self.game, (350, 105, 100, 40), Color.WHITE, "Español", self.set_spanish)
        self.button_russian = Btn(self.game, (350, 155, 100, 40), Color.WHITE, 'Русский', self.set_russian)
        self.button_english = Btn(self.game, (350, 205, 100, 40), Color.WHITE, 'English', self.set_english)
        self.button_german = Btn(self.game, (350, 255, 100, 40), Color.WHITE, 'Deutsch', self.set_german)
        self.button_french = Btn(self.game, (350, 305, 100, 40), Color.WHITE, 'Français', self.set_french)
        self.button_exit = Btn(self.game, (350, 405, 100, 40), Color.WHITE, 'Выход', self.exit)
        self.objects = [self.button_spanish, self.button_exit,  self.button_russian,
                        self.button_english, self.button_german, self.button_french]

    def set_spanish(self):
        file = open('quests/language', 'w')
        file.write('ru')
        file.close()
        self.update_scenes()
        self.set_next_scene(self.game.STATS_SCENE_INDEX)

    def set_russian(self):
        file = open('quests/language', 'w')
        file.write('ru')
        file.close()
        self.update_scenes()
        self.set_next_scene(self.game.STATS_SCENE_INDEX)

    def set_english(self):
        file = open('quests/language', 'w')
        file.write('en')
        file.close()
        self.game.scenes[1] = 0
        self.update_scenes()
        self.set_next_scene(self.game.STATS_SCENE_INDEX)

    def set_german(self):
        file = open('quests/language', 'w')
        file.write('de')
        file.close()
        self.update_scenes()
        self.set_next_scene(self.game.STATS_SCENE_INDEX)

    def set_french(self):
        file = open('quests/language', 'w')
        file.write('fr')
        file.close()
        self.update_scenes()
        self.set_next_scene(self.game.STATS_SCENE_INDEX)

    def update_scenes(self):
        self.game.scenes[self.game.STATS_SCENE_INDEX].create_objects()
        self.game.scenes[self.game.QUEST_SCENE_INDEX].create_objects()
        self.game.scenes[self.game.FRACTION_SCENE_INDEX].create_objects()
        self.game.scenes[self.game.CALL_CONTACT_SCENE_INDEX].create_objects()
        self.game.scenes[self.game.CYB_CONTACT_SCENE_INDEX].create_objects()
        self.game.scenes[self.game.POD_CONTACT_SCENE_INDEX].create_objects()


    def exit(self):
        self.game.game_over = True