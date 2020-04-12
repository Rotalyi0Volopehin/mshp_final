from random import randint

from objects.base import DrawObject


class Ball(DrawObject):

    def __init__(self, game, x=100, y=100):
        super().__init__(game)
        self.x = x
        self.y = y

    def process_draw(self):
        self.game.screen.blit(self.image, self.rect)


class LinearMovingBall(Ball):
    def __init__(self, game):
        super().__init__(game)
        self.window_width = self.game.width
        self.window_height = self.game.height
        self.shift_x = 1 if randint(0, 1) == 1 else -1
        self.shift_y = 1 if randint(0, 1) == 1 else -1
