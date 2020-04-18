import pygame
import sys
from constants import Color
from objects.base import DrawObject
from objects.button import Btn


class TextBar(DrawObject):
    def __init__(self, game, file_name, path_to_file, font_name='Comic Sans', font_size=24, is_bold=True,
                 is_italic=False, color = (255, 255, 255), x=10, y=350, width=780, height=240, func=None):
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
        self.font = pygame.font.SysFont(self.font_name, self.font_size, self.is_bold, self.is_italic)
        self.end = False
        self.lal = 0
        self.is_start = True
        self.buttons = []
        self.next_act = False

    def process_logic(self):
        if not self.end_quest:
            self.set_next_dialog()


    def set_next_dialog(self):
        """Функция которая "перелистывает" страницу диалога"""
        if self.is_start:
            self.lal = 0
            self.is_start = False
            self.data_strings = []
            self.text_frame = ''
            self.text_frame = self.data[self.data.find('<d>', self.now_word_a) + 3:
                                        self.data.find('</d>', self.now_word_a)]
            self.flag = True
            self.now_word_f = 0
            while self.flag:
                self.data_strings.append(self.text_frame[self.text_frame.find('<p>', self.now_word_f) + 3:
                                                         self.text_frame.find('</p>', self.now_word_f)])
                self.now_word_f = self.text_frame.find('</p>', self.now_word_f) + 1
                if self.text_frame.find('</p>', self.now_word_f) == -1:
                    self.flag = False
            self.now_word_a = self.data.find('</d>', self.now_word_a) + 1
        if self.data.find('</d>', self.now_word_a) < 0 and self.lal + 1 == len(self.data_strings) and not self.end:
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
            self.now_word_a = 0
            self.lal = 0
            self.text_frame = ''
            self.data_strings = ['']
            self.flag = True
            self.is_start = True
            self.end = False

    def process_draw(self):
        if not self.end_quest:
            pygame.draw.rect(self.game.screen, Color.GREY_BLUE, (self.x, self.y, self.width, self.height))
            pygame.draw.rect(self.game.screen, Color.GREEN, (self.x, self.y, self.width, self.height), 2)
            pygame.draw.rect(self.game.screen, Color.RED, (self.x + 5, self.y + 5, self.width - 10, self.height - 10), 2)
            for b in self.buttons:
                b.process_draw()
            self.count = 0
            for i in range(self.lal + 1):
                text_surface = self.font.render(self.data_strings[i], True, self.color)
                self.game.screen.blit(text_surface, [self.x + 10, self.y + 10 + self.count])
                self.count += self.font_size

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
        '''Функия создает кнопки


        '''
        self.now_word_b = 0
        self.button_number = 0
        count = self.search_btns(self.data)
        functions = [self.choice_1, self.choice_2, self.choice_3]
        while self.data.find('<btn>', self.now_word_b) != -1:
            button_name = self.data[self.data.find('<btn>', self.now_word_b) + 5:self.data.find('</btn>', self.now_word_b)]
            self.buttons.append(Btn(self.game, (self.x + 10,
                                                self.y + self.height - count * 35 + self.button_number * 35 - 10,
                                                self.width - 20,
                                                30),
                                    Color.GREY_BLUE, button_name, functions[self.button_number]
                                    ))
            self.now_word_b = self.data.find('</btn>', self.now_word_b) + 3
            self.button_number += 1
            print(button_name)

    def choice_1(self):
        if not self.next_act:
            self.set_next_ev('1')
        else:
            self.set_next_ev('')
            self.next_act = False

    def choice_2(self):
        if not self.next_act:
            self.set_next_ev('2')
        else:
            self.set_next_ev('')
            self.next_act = False

    def choice_3(self):
        if not self.next_act:
            self.set_next_ev('3')
        else:
            self.set_next_ev('')
            self.next_act = False

    def end_quest_func(self):
        '''Функция записывает статус игрока


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
        '''Функция обрабатывает конец файла


        или переход к следующей главе
        '''
        if self.data.find('<A') != -1:
            self.act = int(self.data[self.data.find('<A') + 2])
            self.path_to_file = self.path_to_file_qu + 'A' + str(self.act) \
                                + '/' + self.sex + '/'
            print(self.path_to_file, self.file_name)
            self.dialog_index = '0'
            self.next_act = True
        if self.data.find('<END>') != -1:
            self.end_quest = True
        self.end_quest_func()

    def search_btns(self, data):
        """Функия поиска количества кнопок

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