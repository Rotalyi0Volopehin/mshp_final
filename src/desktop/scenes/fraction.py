import os
from constants import Color
from objects.button import Btn
from objects.yandex_translate import Translator
from scenes.base import Scene


class FractionScene(Scene):
    def create_objects(self):
        lang_path = os.path.join("quests", "language")
        file = open(lang_path, 'r')
        language = file.read()
        file.close()
        self.path = os.path.join("quests", "stats")
        translator = Translator()
        self.button_pod = Btn(self.game, (300, 155, 200, 40), Color.WHITE,
                              translator.translate("Подполье", language),
                              self.frac_pod)
        self.button_call = Btn(self.game, (300, 205, 200, 40), Color.BLUE,
                               translator.translate("Зов Свободы", language),
                               self.frac_call)
        self.button_cyb = Btn(self.game, (300, 255, 200, 40), Color.ORANGE,
                              translator.translate("Cyber corp", language),
                              self.frac_cyb)
        self.button_exit = Btn(self.game, (300, 305, 200, 40), Color.WHITE,
                               translator.translate("Выход", language),
                               self.exit)
        self.objects = [self.button_pod, self.button_call, self.button_cyb, self.button_exit]

    def frac_pod(self):
        f = open(self.path, 'a')
        f.write('\n')
        f.write('fraction :' + str("pod") + '|')
        f.write('contacts :' + str("swan") + '|' + '\n')
        f.close()
        self.set_next_scene(self.game.POD_CONTACT_SCENE_INDEX)

    def frac_call(self):
        f = open(self.path, 'a')
        f.write('\n')
        f.write('fraction :' + str("call") + '|')
        f.write('contacts :' + str("swan") + '|' + '\n')
        f.close()
        self.set_next_scene(self.game.CALL_CONTACT_SCENE_INDEX)

    def frac_cyb(self):
        f = open(self.path, 'a')
        f.write('\n')
        f.write('fraction :' + str("cyb") + '|')
        f.write('contacts :' + str("swan") + '|' + '\n')
        f.close()
        self.set_next_scene(self.game.CYB_CONTACT_SCENE_INDEX)

    def exit(self):
        self.game.game_over = True