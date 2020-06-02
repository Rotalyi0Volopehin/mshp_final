import pygame
import os

from constants import Color
from objects.base import DrawObject
from objects.text import Text


class ToolBarCell(DrawObject):
    """Класс ячейки в тулбаре"""
    ERROR_SHAKING_DURATION = 10

    def __init__(self, game, x, y, width, height, num=0, pt_set=None):
        """Инициалихация ячейки"""
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
        self.error_shaking_ticks = 0

    def update_pt_set(self, new_pt_set):
        """Обновление набора инструмента"""
        self.pt_set = new_pt_set
        self.update_count()

    def update_count(self):
        """Обновление количества ингструменитов"""
        text = "x0" if self.pt_set is None else "x" + str(self.pt_set.count)
        self.count_label.update_text(text)

    def process_draw(self):
        """Процесс рисования"""
        self.num_label.process_draw()
        self.count_label.process_draw()
        if self.error_shaking_ticks == 0:
            self.game.screen.blit(self.img, (self.x, self.y))
            pygame.draw.rect(self.game.screen, Color.BLUE, self.geometry, 2)
        else:
            shaking_shift = ((self.error_shaking_ticks & 7) << 1) - 8
            self.game.screen.blit(self.img, (self.x, self.y + shaking_shift))
            geom = (self.x, self.y + shaking_shift, self.width, self.height)
            pygame.draw.rect(self.game.screen, Color.RED, geom, 2)
            self.error_shaking_ticks -= 1

    def process_event(self, event):
        """процесс событий"""
        if event.type == pygame.KEYUP:
            self.on_key_up(event)
        if (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):
            self.on_click(event)

    def on_key_up(self, event):
        """При отпускании кнопки мыши"""
        num = event.key - 48
        if num == self.num:
            self.__try_invoke_function()

    def on_click(self, event):
        """При нажатии на кнопку мыши"""
        if self.rect.collidepoint(event.pos):
            self.__try_invoke_function()

    def __try_invoke_function(self):
        """1"""
        ok = False
        if self.pt_set is not None:
            target_tile = self.game.current_scene.game_vc.grid_vc.target_tile
            if target_tile is not None:
                if self.pt_set.try_use(target_tile):
                    self.error_shaking_ticks = 0
                    self.update_count()
                    ok = True
        if not ok:
            self.error_shaking_ticks = ToolBarCell.ERROR_SHAKING_DURATION

    def set_img(self, img):
        """Установка картинки"""
        self.img = pygame.image.load(img)
