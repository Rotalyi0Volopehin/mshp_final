import user_info

from constants import Color
from scenes.base import Scene
from objects.text import Text
from objects.button import Btn


class GameOverScene(Scene):
    def __init__(self, game, game_model, defeated):
        self.game_model = game_model
        self.defeated = defeated
        super().__init__(game)

    def create_objects(self):
        if not user_info.online:
            text = "Игра окончена"
            color = Color.WHITE
        elif self.game_model.player_ids[user_info.user_id].team.defeated or self.defeated:
            text = "Ваша фракция проиграла"
            color = Color.RED
        else:
            text = "Ваша фракция выиграла"
            color = Color.ORANGE
        game_over_label = Text(self.game, font_size=42, text=text, color=color,
                               x=self.game.width >> 1, y=self.game.height >> 1)
        menu_button = Btn(self.game, (350, 455, 100, 40), text="Меню", function=self.__goto_menu)
        self.objects.extend([game_over_label, menu_button])

    def __goto_menu(self):
        from scenes.main_menu import MainMenuScene
        self.game.set_origin_scene(MainMenuScene)
