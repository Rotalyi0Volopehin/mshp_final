import pygame

from objects.base import DrawObject
from objects.text import Text
from constants import Color
from geometry_tools import triangle_contains_point


class EndTurnButton(DrawObject):
    SPRITES = list()
    SIZE = 64

    @staticmethod
    def render_sprites():
        from game_vc.game_vc import GameVC
        for i in range(3):
            color = GameVC.TEAM_COLORS[i]
            sprite = EndTurnButton.__render_sprite(color)
            EndTurnButton.SPRITES.append(sprite)

    @staticmethod
    def __render_sprite(color) -> pygame.Surface:
        size = EndTurnButton.SIZE
        sprite = pygame.Surface((size, size))
        sprite.set_colorkey(Color.BLACK)
        points = [(size, size >> 1), (0, 0), (0, size)]
        pygame.draw.polygon(sprite, color, points)
        pygame.draw.polygon(sprite, Color.WHITE, points, 3)
        pygame.draw.line(sprite, Color.WHITE, (size - 2, 0), (size - 2, size - 2), 3)
        return sprite

    def __init__(self, game, pos_x, pos_y):
        super().__init__(game)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.time_left = -1
        size = EndTurnButton.SIZE
        self.time_left_label = Text(game, font_size=20, color=Color.WHITE,
                                    x=pos_x + (size // 3), y=pos_y + (size >> 1))
        self.sprite = self.sprite_team = None
        self.points = [
            (size + pos_x, (size >> 1) + pos_y),
            (pos_x, pos_y),
            (pos_x, size + pos_y)
        ]

    def update_time_left(self):
        time_left = int(self.game.current_scene.game_vc.model.turn_time_left)
        if self.time_left != time_left:
            self.time_left = time_left
            self.time_left_label.update_text(str(time_left))

    def update_team(self):
        team = self.game.current_scene.game_vc.model.current_team
        if self.sprite_team != team:
            self.sprite_team = team
            self.sprite = EndTurnButton.SPRITES[team.index]

    def process_draw(self):
        if not hasattr(self.game.current_scene, "game_vc"):
            return
        self.update_time_left()
        self.update_team()
        rect = self.sprite.get_rect()
        rect.x = self.pos_x
        rect.y = self.pos_y
        self.game.screen.blit(self.sprite, rect)
        self.time_left_label.process_draw()

    def process_event(self, event):
        if (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1) and \
                triangle_contains_point(*self.points, event.pos[0], event.pos[1]):
            self.game.current_scene.game_vc.end_turn()


EndTurnButton.render_sprites()
