from constants import Color
from objects.button import Btn
from objects.text_bar import TextBar
from objects.text import Text
from objects.image import Image
from scenes.base import Scene
from objects.yandex_translate import Translator


class QuestScene(Scene):

    def create_objects(self):
        file = open('quests/language', 'r')
        language = file.read()
        file.close()
        file_index = open('quests/index', 'r')
        quest_index = file_index.read()
        file_index.close()
        translator = Translator()
        path_to_file = 'quests/quest_' + quest_index + '/'
        self.text_bar = TextBar(self.game, file_name='text_0', path_to_file=path_to_file, func=self.restart)
        self.button_restart = Btn(self.game, (350, 50, 100, 40), Color.WHITE,
                                  translator.translate("РЕСТАРТ", language), self.restart)
        self.objects.extend([
            self.button_restart,
            self.text_bar,
        ])

    def restart(self):
        f = open('quests/config', 'w')
        f.write('sex: ' + 'M' + '\n')
        f.write('end: False' + '\n')
        f.write('now: ' + '0' + '\n')
        f.write('reputation: ' + '0' + '\n')
        f.write('moral: ' + '0' + '\n')
        f.write('A: ' + '1')
        f.close()
        f = open('quests/stats', 'w')
        f.close()
