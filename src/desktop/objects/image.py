import pygame

from objects.base import DrawObject


class Image(DrawObject):
    def __init__(self, game, file_name=None, x=100, y=100):
        super().__init__(game)
        self.image = pygame.image.load(file_name).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x = x
        self.y = y

    def process_draw(self):
        self.game.screen.blit(self.image, self.rect)
