import pygame

from scenes.base import Scene
from objects.button import Btn
from constants import Color


class MapScene(Scene):
    def create_objects(self):
        button_back = Btn(self.game, (350, 500, 100, 40), Color.WHITE, 'Меню', self.game.return_to_upper_scene)
        self.objects.append(button_back)
        self.game_vc = self.game.current_scene.game_vc
        self.objects.append(self.game_vc)
        emp_button = Btn(self.game, (30, 450, 100, 40), Color.WHITE, 'EMP', self.game_vc.grid_vc.use_ability_emp)
        self.objects.append(emp_button)
        fish_button = Btn(self.game, (30, 500, 100, 40), Color.WHITE, 'Fishing',
                          self.game_vc.grid_vc.use_ability_fishing)
        self.objects.append(fish_button)

