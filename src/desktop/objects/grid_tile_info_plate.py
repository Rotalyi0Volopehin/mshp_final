import pygame

from objects.base import DrawObject
from objects.text import Text, TextAlignment
from constants import Color


class GridTileInfoPlate(DrawObject):
    def __init__(self, game, right_border: int, pos_y: int, height: int):
        super().__init__(game)
        self.right_border = right_border
        self.pos_y = pos_y
        self.width = 0
        self.height = height
        self.vertical_shift = 0
        self.labels = list()
        self.update = False

    def process_draw(self):
        self.try_update_info()
        if self.game.current_scene.game_vc.grid_vc.selected_tile is None:
            return
        for label in self.labels:
            label.process_draw()
        rect = (self.right_border - self.width, self.pos_y, self.width, self.height)
        pygame.draw.rect(self.game.screen, Color.WHITE, rect, 2)

    def process_event(self, event):
        if (event.type == pygame.MOUSEBUTTONUP) or (event.type == pygame.KEYUP):
            self.update = True

    def try_update_info(self):
        if self.update:
            self.update = False
            self.update_labels()

    def update_labels(self):
        tile = self.game.current_scene.game_vc.grid_vc.selected_tile
        if tile is None:
            return
        self.labels.clear()
        content = [
            f"Название : {type(tile).__name__}",
            f"Доход : {tile.owners_income}",
            f"Мощя : {tile.power}/{tile.power_cap} (+{tile.power_growth})",
        ]
        self.__try_create_effects_info(content)
        for content_line in content:
            self.__create_label(content_line)
        self.width = self.__find_max_label_width() + 8
        for i in range(len(self.labels)):
            self.__locate_label(i)
        self.__try_locate_effects_info()

    def __try_create_effects_info(self, content: list):
        tile = self.game.current_scene.game_vc.grid_vc.selected_tile
        if len(tile.effects) > 0:
            content.append("Эффекты:")
            for effect in tile.effects:
                content.append(f"- {type(effect).__name__}")

    def __try_locate_effects_info(self):
        tile = self.game.current_scene.game_vc.grid_vc.selected_tile
        if len(tile.effects) > 0:
            self.labels[3].alignment = TextAlignment.CENTER
            self.labels[3].x = self.right_border - (self.width >> 1)

    def __create_label(self, text: str):
        label = Text(self.game, font_size=20, color=Color.WHITE, text=text, alignment=TextAlignment.LEFT)
        self.labels.append(label)

    def __locate_label(self, ind: int):
        label = self.labels[ind]
        label.x = self.right_border - self.width + 4
        label.y = self.pos_y - self.vertical_shift + ind * label.height + (label.height >> 1)

    def __find_max_label_width(self) -> int:
        max_width = 0
        for label in self.labels:
            if max_width < label.width:
                max_width = label.width
        return max_width
