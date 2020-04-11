import pygame
from constants import Color
from objects.base import DrawObject


class TextBar(DrawObject):
    def __init__(self, game, file_name, font_name='Comic Sans', font_size=24, is_bold=True,
                 is_italic=False, text='Define me!',
                 color=(255, 255, 255), x=10, y=350, width=780, height=240):
        super().__init__(game)
        self.text_index = 0
        self.font_name = font_name
        self.font_size = font_size
        self.is_bold = is_bold
        self.is_italic = is_italic
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.data = text
        self.now_word_a = 0
        self.clicked = False
        self.text_frame = ''
        self.data_strings = []
        self.flag = True
        self.count = 0
        self.rect = pygame.Rect(x, y, width, height)
        self.next = False
        self.font = pygame.font.SysFont(self.font_name, self.font_size, self.is_bold, self.is_italic)
        self.end = False
        self.lal = 0
        self.is_start = True

    def process_logic(self):
        self.set_next_dialog()
        #self.set_next_ev()

    def set_next_dialog(self):
        if self.is_start:
            self.lal = 0
            self.next = False
            self.is_start = False
            self.count = 0
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
            self.end = True
            print("ASD")
            print(self.lal)




    def set_next_ev(self):
        if self.end:
            self.text_index += 1
            self.now_word_a = 0
            self.text_frame = ''
            self.data_strings = []
            self.flag = True
            self.count = 0
            self.end = False


    def process_draw(self):
        pygame.draw.rect(self.game.screen, Color.GREY_BLUE, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(self.game.screen, Color.GREEN, (self.x, self.y, self.width, self.height), 2)
        pygame.draw.rect(self.game.screen, Color.RED, (self.x + 5, self.y + 5, self.width - 10, self.height - 10), 2)
        #for item in self.data_strings:
        self.count = 0
        for i in range(self.lal+1):
            text_surface = self.font.render(self.data_strings[i], True, self.color)
            self.game.screen.blit(text_surface, [self.x + 10, self.y + 10 + self.count])
            self.count += self.font_size


    def process_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.on_click(event)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.on_release(event)

    def on_click(self, event):
        if self.rect.collidepoint(event.pos):
            self.clicked = True

    def on_release(self, event):
        if self.clicked and not self.end:
            if self.lal + 1 >= len(self.data_strings):
                self.is_start = True
            else:
                self.next = True
                self.lal += 1
        self.clicked = False