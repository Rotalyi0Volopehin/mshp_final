from constants import Color
from objects.button import Btn
from objects.yandex_translate import Translator
from objects.advanced_button import AdvBtn

from scenes.base import Scene


class StatsMenuScene(Scene):
    """
    Сцена выбора параметров
    """
    def create_objects(self):
        """
        Создание кнопок в начале игры.
        :return:
        """
        self.current_points = 0
        file = open('quests/language', 'r')
        language = file.read()
        file.close()
        translator = Translator()
        self.strength = AdvBtn(self.game, (320, 25, 160, 70),
                               Color.WHITE, "Физическая сила", self.apply_point, 24)
        self.charisma = AdvBtn(self.game, (320, 105, 160, 70),
                               Color.WHITE, "Харизма", self.apply_point, 24)
        self.dexterity = AdvBtn(self.game, (320, 185, 160, 70),
                                Color.WHITE, "Ловкость", self.apply_point, 24)
        self.savvy = AdvBtn(self.game, (320, 265, 160, 70),
                            Color.WHITE, "Смекалка", self.apply_point, 24)
        self.stealth = AdvBtn(self.game, (320, 345, 160, 70),
                              Color.WHITE, "Скрытность", self.apply_point, 24)
        self.skill_points = Btn(self.game, (150, 500, 200, 40),
                                Color.WHITE,
                                translator.translate("Оставшиеся очки: 0", language), None)
        self.quest = Btn(self.game, (450, 500, 200, 40),
                         Color.WHITE,
                         translator.translate("Начать задания", language), self.set_quest)
        self.objects.extend([self.strength,
                             self.charisma,
                             self.dexterity,
                             self.savvy,
                             self.stealth,
                             self.skill_points,
                             self.quest])

    def set_quest(self):
        """
        Запись характеристик в файл конфига и переход к сцене выбора фракций.
        :return:
        """
        if self.current_points == 0:
            file = open('quests/stats', 'a')
            file.write('\n')
            file.write('str :' + str(self.strength.num) + '|' + '\n')
            file.write('cha :' + str(self.charisma.num) + '|' + '\n')
            file.write('dex :' + str(self.dexterity.num) + '|' + '\n')
            file.write('sav :' + str(self.savvy.num) + '|' + '\n')
            file.write('ste :' + str(self.stealth.num) + '|')
            file.write('fraction :' + str("pod") + '|')
            file.write('contacts :' + str("swan") + '|' + '\n')
            file.close()
            from scenes.quest import QuestScene
            self.game.set_origin_scene(QuestScene)

    def apply_point(self, func=None):
        """
        функция, позволяющая вкладывать очки в характеристику
        :param func:
        :return:
        """
        if func:
            if func == '+':
                self.current_points -= 1
            else:
                self.current_points += 1
        self.skill_points.internal_button.text = "Оставшиеся очки: " + str(self.current_points)
        self.skill_points.internal_button.render_text()
