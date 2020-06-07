import pygame
import sys
import os
from constants import Color
from objects.button import Btn
from objects.yandex_translate import Translator
from third_party.button import Button
from objects.base import DrawObject


class AdvBtn(DrawObject):

    pygame.font.init()

    UP_STYLE = {
        "hover_color": Color.BLUE,
        "font_color": Color.BLACK,
        "clicked_color": Color.GREY_BLUE,
        "clicked_font_color": Color.BLACK,
        "hover_font_color": Color.ORANGE,
        "font": pygame.font.Font(None, 32)
    }

    DOWN_STYLE = {
        "hover_color": Color.BLUE,
        "font_color": Color.BLACK,
        "clicked_color": Color.WHITE,
        "clicked_font_color": Color.BLACK,
        "hover_font_color": Color.ORANGE,
        "font": pygame.font.Font(None, 32)
    }

    def __init__(self, game, geometry=(10, 10, 100, 40), color=(255, 255, 0), text='Test', function=None, num=0):
        super().__init__(game)
        self.height = geometry[3]
        self.width = geometry[2]
        self.num = num
        path = os.path.join('quests', 'language')
        file = open(path, 'r')
        self.language = file.read()
        file.close()
        self.adv_button_translator = Translator()
        self.text = self.adv_button_translator.translate(text, self.language)
        self.function = function
        up_button_geometry = (geometry[0] + geometry[2] + geometry[2] / 40,
                              geometry[1],
                              geometry[2] / 5,
                              geometry[3] / 2)
        down_button_geometry = (geometry[0] + geometry[2] + geometry[2] / 40,
                                geometry[1] + geometry[3] / 2,
                                geometry[2] / 5,
                                geometry[3] / 2)
        self.up_btn = Button(up_button_geometry, Color.GREEN, self.up_func, **AdvBtn.UP_STYLE)
        self.down_btn = Button(down_button_geometry, Color.RED, self.down_func, **AdvBtn.DOWN_STYLE)
        self.btn = Button(geometry, color, function, **Btn.BUTTON_STYLE)
        self.up_btn.text = "+"
        self.up_btn.render_text()
        self.down_btn.text = "-"
        self.down_btn.render_text()
        self.btn.text = self.text + " " + str(self.num)
        self.btn.render_text()

    def process_event(self, event):
        self.up_btn.check_event(event)
        self.down_btn.check_event(event)
        self.btn.check_event(event)

    def process_draw(self):
        self.up_btn.update(self.game.screen)
        self.down_btn.update(self.game.screen)
        self.btn.update(self.game.screen)

    def up_func(self):
        if 0 <= self.num < 100:
            self.num += 1
            self.btn.text = self.text + " " + str(self.num)
            self.btn.render_text()
            self.btn.update(self.game.screen)
            self.function("+")

    def down_func(self):
        if 0 < self.num <= 100:
            self.num -= 1
            self.btn.text = self.text + " " + str(self.num)
            self.btn.render_text()
            self.btn.update(self.game.screen)
            self.function("-")