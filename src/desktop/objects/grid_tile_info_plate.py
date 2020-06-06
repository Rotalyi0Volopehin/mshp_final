import pygame

from os import path
from objects.base import DrawObject
from objects.text import Text, TextAlignment
from constants import Color


class GridTileInfoPlate(DrawObject):
    EFFECTS_CONTENT_LINE_INDEX = 5
    money_pictogram = pygame.image.load(path.join("images", "pictograms", "money.png"))
    power_pictogram = pygame.image.load(path.join("images", "pictograms", "power.png"))

    def __init__(self, game, game_vc, right_border: int, pos_y: int, height: int):
        super().__init__(game)
        self.game_vc = game_vc
        self.right_border = right_border
        self.pos_y = pos_y
        self.width = 0
        self.height = height
        self.labels = list()
        self.update = False
        self.rect_color = None

    def process_draw(self):
        self.try_update_info()
        if self.game_vc.grid_vc.selected_tile is None:
            self.rect_color = None
            return
        if self.rect_color is None:
            return
        rect = (self.right_border - self.width, self.pos_y, self.width, self.height)
        pygame.draw.rect(self.game.screen, self.rect_color, rect, 0)
        pygame.draw.rect(self.game.screen, Color.WHITE, rect, 2)
        for i in range(len(self.labels)):
            label = self.labels[i]
            if label is None:
                x1 = self.right_border - self.width
                x2 = self.right_border
                y = int(self.pos_y + 1.2 * (i + 1) * self.labels[0].height - 4)
                pygame.draw.line(self.game.screen, Color.WHITE, (x1, y), (x2, y), 2)
            else:
                label.process_draw()
        self.__draw_pictogram_before_label_number(2, GridTileInfoPlate.money_pictogram)
        self.__draw_pictogram_before_label_number(3, GridTileInfoPlate.power_pictogram)

    def __draw_pictogram_before_label_number(self, num: int, pict):
        rect = pict.get_rect()
        rect.x = self.labels[num].x
        rect.y = self.labels[num].y - 8
        self.game.screen.blit(pict, rect)

    def process_event(self, event):
        if (event.type == pygame.MOUSEBUTTONUP) or (event.type == pygame.KEYUP):
            self.update = True

    def try_update_info(self):
        if self.update:
            self.update = False
            self.update_labels()

    def update_labels(self):
        tile = self.game_vc.grid_vc.selected_tile
        if tile is None:
            return
        self.labels.clear()
        self.rect_color = self.game_vc.get_team_color(tile.team)
        content = [
            tile.name, None,
            f"   +{tile.owners_income}",
            "   {:0>2x}/{:0>2x} (+{:0>2x})".format(tile.power, tile.power_cap, tile.power_growth),
        ]
        self.__try_create_effects_info(content)
        for content_line in content:
            self.__create_label(content_line)
        self.width = self.__find_max_label_width() + 8
        for i in range(len(self.labels)):
            self.__locate_label(i)
        self.__try_locate_effects_info()

    def __try_create_effects_info(self, content: list):
        tile = self.game_vc.grid_vc.selected_tile
        if len(tile.effects) > 0:
            content.append(None)
            content.append("Эффекты:")
            for effect in tile.effects:
                content.append(f"- {effect.name}")

    def __try_locate_effects_info(self):
        tile = self.game_vc.grid_vc.selected_tile
        if len(tile.effects) > 0:
            effects_label = self.labels[GridTileInfoPlate.EFFECTS_CONTENT_LINE_INDEX]
            effects_label.alignment = TextAlignment.CENTER
            effects_label.x = self.right_border - (self.width >> 1)
            effects_label.y += effects_label.height >> 1

    def __create_label(self, text: str):
        if text is None:
            label = None
        else:
            label = Text(self.game, font_size=20, text=text, alignment=TextAlignment.LEFT)
        self.labels.append(label)

    def __locate_label(self, ind: int):
        label = self.labels[ind]
        if label is not None:
            label.x = self.right_border - self.width + 4
            label.y = int(self.pos_y + 1.2 * ind * label.height + (label.height >> 1))

    def __find_max_label_width(self) -> int:
        max_width = 0
        for label in self.labels:
            if (label is not None) and (max_width < label.width):
                max_width = label.width
        return max_width
