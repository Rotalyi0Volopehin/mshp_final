from scenes.base import Scene
from constants import Color
from objects.button import Btn


class PodContactScene(Scene):
    def create_objects(self):
        self.button_swan = Btn(self.game, (200, 155, 100, 40), Color.WHITE, "Лилия Свон", self.set_swan)
        self.button_finch = Btn(self.game, (200, 205, 100, 40), Color.WHITE, "Скарлет Финч", self.set_finch)
        self.button_krayn = Btn(self.game, (200, 255, 100, 40), Color.WHITE, "Обадайя Крейн", self.set_krayn)
        self.button_smith = Btn(self.game, (200, 305, 100, 40), Color.WHITE, "Салазар Смит", self.set_smith)
        self.button_kurt = Btn(self.game, (450, 155, 100, 40), Color.WHITE, "Курт", self.set_smith)
        self.button_achill = Btn(self.game, (450, 205, 100, 40), Color.WHITE, "Ахилл", self.set_achill)
        self.button_will = Btn(self.game, (450, 255, 100, 40), Color.WHITE, "Уильим Картер", self.set_will)
        self.button_stein = Btn(self.game, (450, 305, 100, 40), Color.WHITE, "Стейн Роккан", self.set_stein)
        self.button_jim = Btn(self.game, (325, 255, 100, 40), Color.WHITE, "Джим Колан", self.set_jim)
        self.button_exit = Btn(self.game, (350, 405, 100, 40), Color.WHITE, 'Выход', self.exit)
        self.objects = [self.button_swan, self.button_exit, self.button_finch, self.button_krayn, self.button_smith,
                        self.button_kurt, self.button_achill, self.button_will, self.button_stein, self.button_jim]

    def set_swan(self):
        f = open('quests/stats', 'a')
        f.write('\n')
        f.write('contacts :' + str("swan") + '|' + '\n')
        f.close()
        self.set_next_scene(self.game.QUEST_SCENE_INDEX)

    def set_finch(self):
        f = open('quests/stats', 'a')
        f.write('\n')
        f.write('contacts :' + str("finch") + '|' + '\n')
        f.close()
        self.set_next_scene(self.game.QUEST_SCENE_INDEX)

    def set_krayn(self):
        f = open('quests/stats', 'a')
        f.write('\n')
        f.write('contacts :' + str("krayn") + '|' + '\n')
        f.close()
        self.set_next_scene(self.game.QUEST_SCENE_INDEX)

    def set_smith(self):
        f = open('quests/stats', 'a')
        f.write('\n')
        f.write('contacts :' + str("smith") + '|' + '\n')
        f.close()
        self.set_next_scene(self.game.QUEST_SCENE_INDEX)

    def set_stein(self):
        f = open('quests/stats', 'a')
        f.write('\n')
        f.write('contacts :' + str("stein") + '|' + '\n')
        f.close()
        self.set_next_scene(self.game.QUEST_SCENE_INDEX)

    def set_will(self):
        f = open('quests/stats', 'a')
        f.write('\n')
        f.write('contacts :' + str("will") + '|' + '\n')
        f.close()
        self.set_next_scene(self.game.QUEST_SCENE_INDEX)

    def set_achill(self):
        f = open('quests/stats', 'a')
        f.write('\n')
        f.write('contacts :' + str("achill") + '|' + '\n')
        f.close()
        self.set_next_scene(self.game.QUEST_SCENE_INDEX)

    def set_jim(self):
        f = open('quests/stats', 'a')
        f.write('\n')
        f.write('contacts :' + str("jim") + '|' + '\n')
        f.close()
        self.set_next_scene(self.game.QUEST_SCENE_INDEX)

    def exit(self):
        self.game.game_over = True