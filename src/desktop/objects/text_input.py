from pygame_textinput import TextInput
from constants import Color
from objects.base import DrawObject
import pygame


class Txtinput(DrawObject):
    BUTTON_STYLE = {
        "hover_color": Color.BLUE,
        "font_color": Color.RED,
        "clicked_color": Color.GREEN,
        "clicked_font_color": Color.BLACK,
        "hover_font_color": Color.ORANGE
    }

    def __init__(self, game, ant, x, y):
        super().__init__(game)
        self.x = x
        self.y = y
        self.internal_txtinput = TextInput(self.game, antialias=ant)

    @staticmethod
    def no_action(self):
        pass

    def process_logic(self):
        pass

    def set_antialias(self, an):
        self.internal_txtinput.antialias = an

    def process_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.x <= event.pos[0] <= self.x + self.internal_txtinput.font_size * 10 and self.y <= event.pos[1] <= self.y + self.internal_txtinput.font_size:
                    self.internal_txtinput.antialias = True
                else:
                    self.internal_txtinput.antialias = False

        if self.internal_txtinput.antialias:
            if self.internal_txtinput.update(event):
                print(self.login.get_text())

    def process_draw(self):
        self.game.screen.blit(self.internal_txtinput.get_surface(), (self.x, self.y))
