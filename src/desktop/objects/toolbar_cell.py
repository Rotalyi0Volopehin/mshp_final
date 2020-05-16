import pygame
import os

from constants import Color
from objects.base import DrawObject
from objects.text import Text


class ToolBarCell(DrawObject):
    def __init__(self, game, x, y, width, height, num=0, pt_set=None):
        super().__init__(game)
        self.pt_set = pt_set
        self.x = x
        self.y = y
        self.num = num
        self.count_label = Text(self.game, x=x + 32, y=y - 16, font_name="Consolas", font_size=20, color=Color.WHITE)
        self.update_count()
        self.num_label = Text(self.game, x=x + 32, y=y + 64 + 16,
                              font_name="Consolas", font_size=20, color=Color.WHITE, text=str(num))
        self.img = pygame.image.load(os.path.join("images", "pt_icons", f"{num}.png"))
        self.width = width
        self.height = height
        self.geometry = (self.x, self.y, self.width, self.height)
        self.rect = pygame.Rect(self.geometry)

    def update_count(self):
        text = "x0" if self.pt_set is None else "x" + str(self.pt_set.count)
        self.count_label.update_text(text)

    def process_draw(self):
        self.num_label.process_draw()
        self.count_label.process_draw()
        self.game.screen.blit(self.img, (self.x, self.y))
        pygame.draw.rect(self.game.screen, (64, 128, 255), self.geometry, 2)

    def process_event(self, event):
        if event.type == pygame.KEYUP:
            self.on_key_up(event)
        if (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):
            self.on_click(event)

    def on_key_up(self, event):
        num = event.key - 48
        if num == self.num:
            self.__try_invoke_function()

    def on_click(self, event):
        if self.rect.collidepoint(event.pos):
            self.__try_invoke_function()

    def __try_invoke_function(self):
        if self.pt_set is not None:
            target_tile = self.game.current_scene.game_vc.grid_vc.target_tile
            if target_tile is not None:
                self.pt_set.try_use(target_tile)
                self.update_count()

    def set_img(self, img):
        self.img = pygame.image.load(img)
