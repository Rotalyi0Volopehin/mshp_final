from constants import Color
from objects.button import Btn
from scenes.base import Scene
from objects.text import Text


class TeamScene(Scene):
    def create_objects(self):
        self.choose_your_team = Text(self.game,'Comic Sans', 35, True, False, 'Выбери свою команду', Color.WHITE,
                                     400, 150)
        self.button_CC = Btn(self.game, (250, 305, 100, 40), Color.WHITE, "Cyber Corp", self.set_team_cc)
        self.button_LC = Btn(self.game, (350, 305, 100, 40), Color.GREEN, 'Зов свободы', self.set_team_lc)
        self.button_UN = Btn(self.game, (450, 305, 100, 40), Color.ORANGE, 'Подполье', self.set_team_un)
        self.objects = [self.button_CC, self.button_LC, self.button_UN, self.choose_your_team]

    def set_team_cc(self):
        self.game.team = Color.GRAY
        self.set_next_scene(self.game.MAP_SCENE_INDEX)

    def set_team_lc(self):
        self.game.team = Color.DARK_GREEN
        self.set_next_scene(self.game.MAP_SCENE_INDEX)

    def set_team_un(self):
        self.game.team = Color.DARK_ORANGE
        self.set_next_scene(self.game.MAP_SCENE_INDEX)
