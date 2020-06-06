from scenes.base import Scene
from constants import Color
from objects.button import Btn


class CybContactScene(Scene):
    def create_objects(self):
        self.button_swan = Btn(self.game, (350, 155, 100, 40), Color.WHITE, "Лилия Свон", self.set_swan)
        self.button_finch = Btn(self.game, (350, 205, 100, 40), Color.WHITE, "Скарлет Финч", self.set_finch)
        self.button_krayn = Btn(self.game, (350, 255, 100, 40), Color.WHITE, "Обадайя Крейн", self.set_krayn)
        self.button_smith = Btn(self.game, (350, 305, 100, 40), Color.WHITE, "Салазар Смит", self.set_smith)
        self.button_stein = Btn(self.game, (450, 180, 100, 40), Color.WHITE, "Стейн Роккан", self.set_stein)
        self.button_jonson = Btn(self.game, (450, 280, 100, 40), Color.WHITE, "Мистер Джонсон", self.set_jonson)
        self.button_exit = Btn(self.game, (350, 405, 100, 40), Color.WHITE, 'Выход', self.exit)
        self.objects = [self.button_swan, self.button_exit, self.button_finch, self.button_krayn, self.button_smith,
                        self.button_stein, self.button_jonson]

    def set_swan(self):
        f = open('quests/stats', 'a')
        f.write('\n')
        f.write('contacts :' + str("swan") + '|' + '\n')
        f.close()
        self.set_next_scene(self.game.QUEST_MENU_SCENE_INDEX)

    def set_finch(self):
        f = open('quests/stats', 'a')
        f.write('\n')
        f.write('contacts :' + str("finch") + '|' + '\n')
        f.close()
        self.set_next_scene(self.game.QUEST_MENU_SCENE_INDEX)

    def set_krayn(self):
        f = open('quests/stats', 'a')
        f.write('\n')
        f.write('contacts :' + str("krayn") + '|' + '\n')
        f.close()
        self.set_next_scene(self.game.QUEST_MENU_SCENE_INDEX)

    def set_smith(self):
        f = open('quests/stats', 'a')
        f.write('\n')
        f.write('contacts :' + str("smith") + '|' + '\n')
        f.close()
        self.set_next_scene(self.game.QUEST_MENU_SCENE_INDEX)

    def set_stein(self):
        f = open('quests/stats', 'a')
        f.write('\n')
        f.write('contacts :' + str("stein") + '|' + '\n')
        f.close()
        self.set_next_scene(self.game.QUEST_MENU_SCENE_INDEX)

    def set_jonson(self):
        f = open('quests/stats', 'a')
        f.write('\n')
        f.write('contacts :' + str("jonson") + '|' + '\n')
        f.close()
        self.set_next_scene(self.game.QUEST_MENU_SCENE_INDEX)

    def exit(self):
        self.game.game_over = True