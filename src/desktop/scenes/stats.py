from constants import Color
from objects.button import Btn
from scenes.base import Scene
from objects.advanced_button import AdvBtn


class StatsMenuScene(Scene):
    def create_objects(self):
        self.current_points = 0
        self.strength = AdvBtn(self.game, (320, 25, 160, 70), Color.WHITE, "Сила", self.apply_point, 24)
        self.charisma = AdvBtn(self.game, (320, 105, 160, 70), Color.WHITE, "Харизма", self.apply_point, 24)
        self.dexterity = AdvBtn(self.game, (320, 185, 160, 70), Color.WHITE, "Ловкость", self.apply_point, 24)
        self.savvy = AdvBtn(self.game, (320, 265, 160, 70), Color.WHITE, "Смекалка", self.apply_point, 24)
        self.stealth = AdvBtn(self.game, (320, 345, 160, 70), Color.WHITE, "Скрытность", self.apply_point, 24)
        self.skill_points = Btn(self.game, (150, 500, 200, 40), Color.WHITE, "Оставшиеся очки: 0", None)
        self.button_back = Btn(self.game, (350, 500, 100, 40), Color.WHITE, "Меню", self.back_to_menu)
        self.quest = Btn(self.game, (450, 500, 100, 40), Color.WHITE, "Начать задания", self.set_quest_1)

        self.objects = [self.strength, self.charisma, self.dexterity, self.savvy, self.stealth,
                        self.button_back, self.skill_points, self.quest]

    def back_to_menu(self):
        self.set_next_scene(self.game.MENU_SCENE_INDEX)

    def set_quest_1(self):
        if self.current_points == 0:
            self.set_next_scene(self.game.QUEST_SCENE_INDEX)
            f = open('quests/config', 'a')
            f.write('\n')
            f.write('str :' + str(self.strength.num) + '|' + '\n')
            f.write('cha :' + str(self.charisma.num) + '|' + '\n')
            f.write('dex :' + str(self.dexterity.num) + '|' + '\n')
            f.write('sav :' + str(self.savvy.num) + '|' + '\n')
            f.write('ste :' + str(self.stealth.num) + '|')
            f.close()

    def apply_point(self, func=None):
        if func:
            if func == '+':
                self.current_points -= 1
            else:
                self.current_points += 1
        self.skill_points.internal_button.text = "Оставшиеся очки: " + str(self.current_points)
        self.skill_points.internal_button.render_text()