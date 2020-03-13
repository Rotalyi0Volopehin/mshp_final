from network_confrontation.src.desktop.constants import Color
from network_confrontation.src.desktop.objects.button import Btn
from network_confrontation.src.desktop.scenes.base import Scene
from network_confrontation.src.desktop.objects.hex_grid import Grid

class MapScene(Scene):
    def create_objects(self):
        self.map = Grid(self.game,20,8,8,2000)
        self.objects = [self.map]
        print("LOX")

    def set_main_scene(self):
        self.set_next_scene(self.game.MAIN_SCENE_INDEX)

    def set_map_scene(self):
        self.set_next_scene(self.game.MAP_SCENE_INDEX)

    def set_quest_scene(self):
        self.set_next_scene(self.game.QUESTS_SCENE_INDEX)

    def exit(self):
        self.game.game_over = True

