from scenes.base import Scene
from objects.button import Btn
from constants import Color
from objects.toolbar import ToolBar
from objects.end_turn_button import EndTurnButton
from objects.current_player_plate import CurrentPlayerPlate
from objects.grid_tile_info_plate import GridTileInfoPlate
from game_vc.game_vc import GameVC


class MapScene(Scene):
    def __init__(self, game, gs=None):
        self.game_model = gs
        super().__init__(game)

    def create_objects(self):
        width = self.game.width
        height = self.game.height
        self.upgrade_button = Btn(self.game, (width - 240, 5, 100, 40), Color.WHITE, 'Прокачка', self.__set_tech_scene)
        self.game_vc = GameVC(self.game, self.game_model)
        self.game_model = self.game_vc.model
        self.objects.append(self.game_vc)
        toolbar_geom = (35, height - 100, width - 70, 80)
        self.toolbar = ToolBar(self.game, toolbar_geom, self.game_model)
        self.objects.append(self.toolbar)
        self.end_turn_button = EndTurnButton(self.game, width - 100, height - 200)
        self.objects.append(self.end_turn_button)
        current_player_plate = CurrentPlayerPlate(self.game, width - 90, height - 183)
        self.objects.append(current_player_plate)
        grid_tile_info_plate = GridTileInfoPlate(self.game, self.game_vc, width - 20, 50, 340)
        self.objects.append(grid_tile_info_plate)

    def __set_tech_scene(self):
        from scenes.tech_tree import TreeScene
        self.game.goto_deeper_scene(TreeScene)

    def process_all_draw(self):
        can_upgrade = self.can_upgrade
        if can_upgrade:
            self.objects.append(self.upgrade_button)
        super().process_all_draw()
        if can_upgrade:
            self.objects.pop()

    def process_all_events(self, eventlist):
        is_downgrade = self.can_upgrade
        if is_downgrade:
            self.objects.append(self.upgrade_button)
        super().process_all_events(eventlist)
        if is_downgrade:
            self.objects.pop()

    @property
    def can_upgrade(self):
        return self.game_vc.grid_vc.selected_tile is not None