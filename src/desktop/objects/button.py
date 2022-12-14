import pygame

from constants import Color
from objects.base import DrawObject
from third_party.button import Button


class Btn(DrawObject):
    DEFAULT_FONT = pygame.font.Font(None, 16)

    BUTTON_STYLE = {
        "hover_color": Color.BLUE,
        "font_color": Color.RED,
        "clicked_color": Color.GREEN,
        "clicked_font_color": Color.BLACK,
        "hover_font_color": Color.ORANGE,
    }

    def __init__(self, game, geometry=(10, 10, 100, 40), color=Color.BG_GRAY2, text='Test', function=None,
                 font=DEFAULT_FONT):
        super().__init__(game)
        self.geometry = geometry
        self.color = color
        self.function = function if function else Btn.no_action
        self.internal_button = Button(self.geometry, self.color, self.function, **Btn.BUTTON_STYLE, font=font)
        self.internal_button.text = text
        self.internal_button.render_text()

    @staticmethod
    def no_action():
        pass

    def process_event(self, event):
        self.internal_button.check_event(event)

    def process_draw(self):
        self.internal_button.update(self.game.screen)