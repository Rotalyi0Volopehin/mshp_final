import pygame

from constants import Color
from objects.base import DrawObject


class PlayerInfo(DrawObject):
    def __init__(self, game, font_name='Comic Sans', font_size=27, name = "Guest", lvl = "999",
                 color=(255, 255, 255), x=500, y=10):
        super().__init__(game)
        self.font_name = font_name
        self.font_size = font_size
        self.color = color
        self.x = x
        self.width = 290
        self.height = font_size * 2 + 5
        self.y = y
        self.font = pygame.font.SysFont(self.font_name, self.font_size)
        self.update_text(name, lvl)

    def update_text(self, name, lvl):
        self.name = str(name)
        self.lvl = str(lvl)
        self.name_surface = self.font.render('Name: ' + self.name, True, self.color)
        self.lvl_surface = self.font.render('LVL: ' + self.lvl, True, self.color)


    def process_draw(self):
        pygame.draw.rect(self.game.screen, Color.B_GREY, (self.x, self.y, self.width , self.height))
        pygame.draw.rect(self.game.screen, Color.BLUE, (self.x, self.y, self.width , self.height), 2)
        self.game.screen.blit(self.name_surface, (self.x + 10, self.y + 10))
        self.game.screen.blit(self.lvl_surface, (self.x + 10, self.y + self.font_size + 10))