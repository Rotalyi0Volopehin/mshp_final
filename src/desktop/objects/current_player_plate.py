from objects.base import DrawObject
from objects.text import Text
from constants import Color


class CurrentPlayerPlate(DrawObject):
    def __init__(self, game, right_border, pos_y):
        super().__init__(game)
        self.right_border = right_border
        self.pos_y = pos_y
        self.team = None
        self.team_label = Text(game, font_size=20, color=Color.WHITE, y=pos_y)
        self.player = None
        self.player_label = Text(game, font_size=20, color=Color.WHITE, y=pos_y + 32)

    def update_team_label(self):
        team = self.game.current_scene.game_vc.model.current_team
        if self.team != team:
            self.team = team
            self.team_label.update_text(team.name)
            self.team_label.x = self.right_border - (self.team_label.width >> 1) - 20

    def update_player_label(self):
        player = self.game.current_scene.game_vc.model.current_player
        if self.player != player:
            self.player = player
            self.player_label.update_text(player.name)
            self.player_label.x = self.right_border - (self.player_label.width >> 1) - 20

    def process_draw(self):
        if not hasattr(self.game.current_scene, "game_vc"):
            return
        self.update_team_label()
        self.update_player_label()
        self.team_label.process_draw()
        self.player_label.process_draw()
