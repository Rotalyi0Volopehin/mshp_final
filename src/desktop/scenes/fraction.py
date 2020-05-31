from constants import Color
from objects.button import Btn
from scenes.base import Scene


class FractionScene(Scene):
    def create_objects(self):
        self.button_pod = Btn(self.game, (350, 155, 100, 40), Color.WHITE, "Подполье", self.frac_pod)
        self.button_call = Btn(self.game, (350, 205, 100, 40), Color.BLUE, "Зов Свободы", self.frac_call)
        self.button_cyb = Btn(self.game, (350, 255, 100, 40), Color.ORANGE, "Cyber corp", self.frac_cyb)
        self.button_exit = Btn(self.game, (350, 305, 100, 40), Color.WHITE, 'Выход', self.exit)
        self.objects = [self.button_pod, self.button_call, self.button_cyb, self.button_exit]

    def frac_pod(self):
        f = open('quests/stats', 'a')
        f.write('\n')
        f.write('fraction :' + str("pod") + '|')
        f.close()
        self.set_next_scene(self.game.POD_CONTACT_SCENE_INDEX)

    def frac_call(self):
        f = open('quests/stats', 'a')
        f.write('\n')
        f.write('fraction :' + str("call") + '|')
        f.close()
        self.set_next_scene(self.game.CALL_CONTACT_SCENE_INDEX)

    def frac_cyb(self):
        f = open('quests/stats', 'a')
        f.write('\n')
        f.write('fraction :' + str("cyb") + '|')
        f.close()
        self.set_next_scene(self.game.CYB_CONTACT_SCENE_INDEX)

    def exit(self):
        self.game.game_over = True