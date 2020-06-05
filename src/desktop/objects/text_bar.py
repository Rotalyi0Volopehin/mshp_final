import pygame
from constants import Color
from objects.base import DrawObject
from objects.button import Btn
from objects.req_handler import ReqHandler
from objects.yandex_translate import Translator


class TextBar(DrawObject):
    def __init__(self, game, file_name, path_to_file,
                 font_name='Comic Sans', font_size=24, is_bold=True,
                 is_italic=False, color=(255, 255, 255),
                 x=10, y=350, width=780, height=240, func=None):
        super().__init__(game)
        file = open('quests/config', 'r')
        self.sex = str(file.readline().split()[1])
        self.end_quest = file.readline().split()[1]
        if self.end_quest == 'True':
            self.end_quest = True
        else:
            self.end_quest = False
        self.dialog_index = str(file.readline().split()[1])
        self.reputation = int(file.readline().split()[1])
        self.moral = int(file.readline().split()[1])
        self.act = int(file.readline().split()[1])
        file.close()
        print("INIT")
        self.color = color
        self.func = func
        self.path_to_file_qu = path_to_file
        self.path_to_file = path_to_file + 'A' + str(self.act) \
                                         + '/' + self.sex + '/'
        print(self.path_to_file)
        self.file_name = file_name[0:len(file_name) - 1]
        self.font_name = font_name
        self.font_size = font_size
        self.is_bold = is_bold
        self.is_italic = is_italic
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.data = self.get_data_ff(self.path_to_file, self.file_name, self.dialog_index)
        self.now_word_a = 0
        self.clicked = False
        self.text_frame = ''
        self.data_strings = []
        self.flag = True
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.SysFont(self.font_name, self.font_size,
                                        self.is_bold, self.is_italic)
        self.end = False
        self.lal = 0
        self.is_start = True
        self.buttons = []
        self.moral_choices_costs = []
        self.reputation_choices_costs = []
        self.next_act = False
        self.now_word_b = 0
        self.now_word_f = 0
        self.req_handler = ReqHandler(self.data)
        file = open('quests/language', 'r')
        self.language = file.read()
        file.close()
        self.translator = Translator()

    def process_logic(self):
        if not self.end_quest:
            self.set_next_dialog()

    def set_next_dialog(self):
        """Функция которая "перелистывает" страницу диалога"""
        if self.is_start:
            self.lal = 0
            self.is_start = False
            self.now_word_f = 0
            self.data_strings = []
            self.text_frame = ''
            self.text_frame = self.data[self.data.find('<d>', self.now_word_a) + 3:
                                        self.data.find('</d>', self.now_word_a)]
            self.flag = True
            while self.flag:
                dialog_string = self.text_frame[self.text_frame.find('<p>',
                                                self.now_word_f) + 3:
                                                self.text_frame.find('</p>',
                                                self.now_word_f)]
                self.game.translator.update_translation_data(dialog_string, self.language)
                self.data_strings.append(self.game.translator.translate())
                self.now_word_f = self.text_frame.find('</p>', self.now_word_f) + 1
                if self.text_frame.find('</p>', self.now_word_f) == -1:
                    self.flag = False
            self.now_word_a = self.data.find('</d>', self.now_word_a) + 1
        if self.data.find('</d>', self.now_word_a) < 0 and \
                self.lal + 1 == len(self.data_strings) and \
                not self.end:
            self.choose_option()
            self.set_next_option()
            self.end = True

    def set_next_ev(self, choice):
        """Функция которая открывает новый файл


        """
        self.dialog_index += choice
        print(self.dialog_index)
        self.data = self.get_data_ff(self.path_to_file, self.file_name, self.dialog_index)
        if not self.end_quest:
            print("NEW FILE")
            self.buttons.clear()
            self.moral_choices_costs.clear()
            self.now_word_a = 0
            self.lal = 0
            self.text_frame = ''
            self.data_strings = ['']
            self.flag = True
            self.is_start = True
            self.end = False

    def process_draw(self):
        if not self.end_quest:
            pygame.draw.rect(self.game.screen, Color.GREY_BLUE,
                             (self.x, self.y, self.width, self.height))
            pygame.draw.rect(self.game.screen, Color.GREEN,
                             (self.x, self.y, self.width, self.height), 2)
            pygame.draw.rect(self.game.screen, Color.RED,
                             (self.x + 5, self.y + 5, self.width - 10, self.height - 10), 2)
            for b in self.buttons:
                b.process_draw()
            count = 0
            for i in range(self.lal + 1):
                text_surface = self.font.render(self.data_strings[i], True, self.color)
                self.game.screen.blit(text_surface, [self.x + 10, self.y + 10 + count])
                count += self.font_size
            moral_text = self.font.render('Мораль: ' + str(self.moral), True, self.color)
            reputation_text = self.font.render('Репутация: ' + str(self.reputation), True, self.color)
            self.game.screen.blit(moral_text, [self.game.width - 150, 40])
            self.game.screen.blit(reputation_text, [self.game.width - 150, 60])

    def process_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.on_click(event)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.on_release(event)
        for b in self.buttons:
            b.process_event(event)

    def on_click(self, event):
        if self.rect.collidepoint(event.pos):
            self.clicked = True

    def on_release(self, event):
        if self.clicked and not self.end:
            if self.lal + 1 >= len(self.data_strings):
                self.is_start = True
            else:
                self.lal += 1
        self.clicked = False

    def get_data_ff(self, a, b, c):
        """Функция читающая весь текст из нового файла


        возврщает весть текст файла если такое возможно
        :param a:
        :param b:
        :param c:
        :return: data
        """
        try:
            file1 = open(a + b + str(c), 'r')
        except FileNotFoundError or UnboundLocalError or self.end_quest:
            print("END OF JOURNEY")
            self.dialog_index = self.dialog_index[0:len(self.dialog_index) - 1]
            self.func()
            self.end_quest = True
        finally:
            if not self.end_quest:
                stri = file1.read()
                file1.close()
                return stri
            else:
                self.end_quest_func()

    def choose_option(self):
        '''
        Функия создает кнопки
        '''
        button_number = 0
        count = self.search_btns(self.data)
        functions = [self.choice_1, self.choice_2, self.choice_3]
        self.req_handler = ReqHandler(self.data)
        while self.data.find('<btn>', self.now_word_b) != -1:
            color = Color.GREY_BLUE
            self.req_handler.find_requirements(self.data.find('</btn>', self.now_word_b) + 3)
            flag = self.req_handler.check_requirements()
            if flag == 0:
                color = Color.DARK_GREEN
            elif flag == 1:
                color = Color.DARK_RED
                functions[button_number] = self.prohibition
            button_name = self.data[self.data.find('<btn>', self.now_word_b) + 5:
                                    self.data.find('</btn>', self.now_word_b)]
            self.game.translator.update_translation_data(button_name, self.language)
            button_name = self.game.translator.translate()
            self.buttons.append(Btn(self.game, (self.x + 10,
                                                self.y + self.height - count * 35 +
                                                button_number * 35 - 10,
                                                self.width - 20,
                                                30),
                                    color, button_name, functions[button_number]
                                    ))
            functions[button_number] = self.choice_1
            self.now_word_b = self.data.find('</btn>', self.now_word_b) + 3
            if self.data.find('[M', self.now_word_b, self.now_word_b + 6) != -1:
                self.moral_choices_costs.append(self.data[self.data.find('[M', self.now_word_b) + 2:
                                                          self.data.find(']', self.data.find('[M', self.now_word_b))])
            if self.data.find('[R', self.now_word_b, self.now_word_b + 15) != -1:
                print("MORALEMORALE!")
                self.reputation_choices_costs.append(self.data[self.data.find('[R', self.now_word_b) + 2:
                                                     self.data.find(']', self.data.find('[R', self.now_word_b))])
            button_number += 1
            print(button_name)

    def choice_1(self):
        """
        Переход на первую ветку выбора
        с соответсвующими изменениями морали и репутации

        """
        if not self.next_act:
            self.apply_moral(1)
            self.apply_reputation(1)
            self.set_next_ev('1')
        else:
            self.set_next_ev('')
            self.next_act = False

    def choice_2(self):
        """
        Переход на первую ветку выбора
        с соответсвующими изменениями морали и репутации

        """
        if not self.next_act:
            self.apply_moral(2)
            self.apply_reputation(2)
            self.set_next_ev('2')
        else:
            self.set_next_ev('')
            self.next_act = False

    def choice_3(self):
        """
        Переход на первую ветку выбора
        с соответсвующими изменениями морали и репутации

        """
        if not self.next_act:
            self.apply_moral(3)
            self.apply_reputation(3)
            self.set_next_ev('3')
        else:
            self.set_next_ev('')
            self.next_act = False

    def end_quest_func(self):
        '''
        Функция записывает статус игрока
        в момент когда игрока кикают с квеста или он переходит к следующей главе
        '''
        f = open('quests/config', 'w')
        f.write('sex: ' + str(self.sex) + '\n')
        if self.end_quest:
            f.write('end: True' + '\n')
        else:
            f.write('end: False' + '\n')
        f.write('now: ' + str(self.dialog_index) + '\n')
        f.write('reputation: ' + str(self.reputation) + '\n')
        f.write('moral: ' + str(self.moral) + '\n')
        f.write('A: ' + str(self.act))
        f.close()

    def set_next_option(self):
        '''
        Функция обрабатывает конец файла


        или переход к следующей главе
        '''
        if self.data.find('<A') != -1:
            self.act = int(self.data[self.data.find('<A') + 2])
            self.path_to_file = self.path_to_file_qu + 'A' + str(self.act) \
                                + '/' + self.sex + '/'
            #print(self.path_to_file, self.file_name)
            self.dialog_index = '0'
            self.next_act = True
        if self.data.find('<END>') != -1:
            self.end_quest = True
        self.end_quest_func()

    def search_btns(self, data):
        """
        Функия поиска количества кнопок

        в данном файле
        :param: data
        :return: количество кнопок

        """
        ind = 0
        count = 0
        while data.find("<btn>", ind) != -1:
            count += 1
            ind = data.find("<btn>", ind) + 3
        return count

    def apply_moral(self, choice_num):
        """
        Обновляет параметр морали в заваисимости от выбора
        :param choice_num:
        :return:
        """
        if choice_num <= len(self.moral_choices_costs):
            if self.moral_choices_costs[choice_num - 1][0] == '+':
                self.moral += int(self.moral_choices_costs[choice_num - 1]
                                  [1:len(self.moral_choices_costs[choice_num - 1])])
            else:
                self.moral -= int(self.moral_choices_costs[choice_num - 1]
                                  [1:len(self.moral_choices_costs[choice_num - 1])])

    def apply_reputation(self, choice_num):
        """
        Обновляет параметр репутации в заваисимости от выбора
        :param choice_num:
        :return: None
        """
        if choice_num <= len(self.reputation_choices_costs):
            if self.reputation_choices_costs[choice_num - 1][0] == '+':
                self.reputation += int(self.reputation_choices_costs[choice_num - 1]
                                       [1:len(self.reputation_choices_costs[choice_num - 1])])
            else:
                self.reputation -= int(self.reputation_choices_costs[choice_num - 1]
                                       [1:len(self.reputation_choices_costs[choice_num - 1])])

    def prohibition(self):
        """
          Функция, вызываемая при недостатке параметра
          Запрещает перейти дальше
        """
