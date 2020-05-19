import pygame

from objects.base import DrawObject
from enum import Enum


class TextAlignment(Enum):
    CENTER = "center"
    LEFT = "topleft"
    RIGHT = "topright"


class Text(DrawObject):
    def __init__(self, game, font_name="Consolas", font_size=35, is_bold=True, is_italic=False, text='Define me!',
                 color=(255, 255, 255), x=100, y=100, alignment: TextAlignment = TextAlignment.CENTER):
        super().__init__(game)
        self.font_name = font_name
        self.font_size = font_size
        self.is_bold = is_bold
        self.is_italic = is_italic
        self.color = color
        self.x = x
        self.y = y
        self.alignment = alignment
        self.font = pygame.font.SysFont(self.font_name, self.font_size, self.is_bold, self.is_italic)
        self.update_text(text)

    def update_text(self, text):
        self.text = str(text)
        self.text_surface = self.font.render(self.text, True, self.color)

    @property
    def width(self) -> int:
        return self.text_surface.get_width()

    @property
    def height(self) -> int:
        return self.text_surface.get_height()

    def process_draw(self):
        params = {self.alignment.value: (self.x, self.y)}
        self.game.screen.blit(self.text_surface, self.text_surface.get_rect(**params))
