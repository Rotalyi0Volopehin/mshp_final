import os
from constants import Color
from objects.button import Btn
from objects.text_bar import TextBar
from objects.text import Text
from objects.image import Image
from scenes.base import Scene
from objects.yandex_translate import Translator


class QuestScene(Scene):
    def create_objects(self):
        lang_path = os.path.join('quests', 'language')
        file = open(lang_path, 'r')
        self.language = file.read()
        file.close()
        index_path = os.path.join('quests', 'index')
        file_index = open(index_path, 'r')
        quest_index = file_index.read()
        file_index.close()
        self.translator = Translator()
        path_to_file = os.path.join('quests', 'quest_' + quest_index, '')
        self.text_bar = TextBar(self.game, file_name='text_0', path_to_file=path_to_file, func=self.restart,
                                fail_func=self.fail_func, win_func=self.win_func, end_func=self.end_func)
        menu_button = Btn(self.game, (550, 20, 100, 40),
                                  text=self.translator.translate("Заново", self.language), function=self.restart)
        self.message_label = Text(self.game, text="", x=self.game.width >> 1)
        self.objects.extend([
            menu_button,
            self.text_bar,
            self.message_label,
        ])

    def fail_func(self):
        self.message_label.update_text(self.translator.translate("Миссия провалена", self.language))

    def win_func(self):
        self.message_label.update_text(self.translator.translate("Миссия выполнена. +опыт", self.language))

    def end_func(self):
        self.message_label.update_text(self.translator.translate("Конец", self.language))

    def restart(self):
        config_path = os.path.join('quests', 'config')
        f = open(config_path, 'w')
        f.write('sex: ' + 'M' + '\n')
        f.write('end: False' + '\n')
        f.write('now: ' + '0' + '\n')
        f.write('reputation: ' + '0' + '\n')
        f.write('moral: ' + '0' + '\n')
        f.write('A: ' + '1')
        f.close()
        stat_path = os.path.join('quests', 'stats')
        f = open(stat_path, 'w')
        f.close()
        self.game.set_origin_scene(QuestScene)
