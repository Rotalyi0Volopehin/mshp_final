import pygame as pg
from constants import Color
from objects.base import DrawObject
from objects.text import Text


class ToolBarCell(DrawObject):
    def __init__(self, game, x, y, width, height, num=0, function=None):
        self.game = game
        super().__init__(game)
        self.function = function
        self.x = x
        self.num = num
        self.num = Text(self.game, font_name="Consolas", font_size=20, color=Color.WHITE, x=x + 32, y=y + 64 + 16,
                        text=str(self.num))
        self.y = y
        self.img = pg.image.load('images/no_ability.png')
        # self.img_rect = self.img.get_rect(x, y)
        self.width = width
        self.height = height
        self.geometry = (self.x, self.y, self.width, self.height)
        self.rect = pg.Rect(self.geometry)
        self.clicked = False

    def process_draw(self):
        self.num.process_draw()
        self.game.screen.blit(self.img, (self.x, self.y))
        pg.draw.rect(self.game.screen, (64, 128, 255), self.geometry, 2)

    def process_event(self, event):
        if event.type == pg.KEYDOWN and callable(self.function):
            self.function()
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            self.on_click(event)

    def on_click(self, event):
        if self.rect.collidepoint(event.pos) and callable(self.function):
            self.function()

    def set_img(self, img):
        self.img = pg.image.load(img)
