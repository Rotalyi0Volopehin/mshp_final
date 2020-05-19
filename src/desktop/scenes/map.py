from scenes.base import Scene
from objects.button import Btn
from objects.text import Text
from constants import Color
from objects.toolbar import ToolBar
from objects.end_turn_button import EndTurnButton
from objects.current_player_plate import CurrentPlayerPlate
from objects.grid_tile_info_plate import GridTileInfoPlate


class MapScene(Scene):
    def create_objects(self):
        width = self.game.width
        height = self.game.height
        button_back = Btn(self.game, (width - 120, 5, 100, 40), Color.WHITE, 'Меню', self.game.return_to_upper_scene)
        self.objects.append(button_back)
        self.game_vc = self.game.current_scene.game_vc
        self.objects.append(self.game_vc)
        toolbar_geom = (35, height - 100, width - 70, 80)
        self.toolbar = ToolBar(self.game, toolbar_geom)
        self.objects.append(self.toolbar)
        self.end_turn_button = EndTurnButton(self.game, width - 100, height - 200)
        self.objects.append(self.end_turn_button)
        current_player_plate = CurrentPlayerPlate(self.game, width - 90, height - 183)
        self.objects.append(current_player_plate)
        grid_tile_info_plate = GridTileInfoPlate(self.game, width - 20, 50, 300)
        self.objects.append(grid_tile_info_plate)
        self.__init_controls()

    def __init_controls(self):
        controls = [
            "ЛКМ - выделение",
            "зажатие ЛКМ - выделение соседа",
            "колёсико/вверх/вниз/end/home - перемещение мощи",
            "С - снятие выделения",
            "цифры - применение ИВ"
        ]
        for i in range(len(controls)):
            line = controls[i]
            text = Text(self.game, font_name="Consolas", font_size=20, color=Color.WHITE, x=300, y=250 + i * 20,
                        text=line)
            self.objects.append(text)

