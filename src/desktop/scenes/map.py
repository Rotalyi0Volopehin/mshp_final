from scenes.base import Scene
from objects.button import Btn
from objects.text import Text
from constants import Color
from objects.toolbar import ToolBar
from objects.end_turn_button import EndTurnButton


class MapScene(Scene):
    def create_objects(self):
        button_back = Btn(self.game, (350, 420, 100, 40), Color.WHITE, 'Меню', self.game.return_to_upper_scene)
        self.objects.append(button_back)
        self.game_vc = self.game.current_scene.game_vc
        self.objects.append(self.game_vc)
        toolbar_geom = (35, self.game.height - 100, self.game.width - 70, 80)
        self.toolbar = ToolBar(self.game, toolbar_geom)
        self.objects.append(self.toolbar)
        self.end_turn_button = EndTurnButton(self.game, self.game.width - 100, self.game.height - 200)
        self.objects.append(self.end_turn_button)
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

