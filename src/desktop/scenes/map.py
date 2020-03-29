from constants import Color
from objects.button import Btn
from scenes.base import Scene
from objects.hex_grid import Grid
from objects.text import Text

class MapScene(Scene):
    def create_objects(self):
        self.map = Grid(self.game, 20, 8, 8, 1200, 4)
        self.instruction1 = Text(self.game,x=200,y=250, text="Инструкция")
        self.instruction2 = Text(self.game,x=250,y=300, text="1 Выбери клетку кликом мыши")
        self.instruction21 = Text(self.game, x=400, y=350, text="1.1 Красная - твоя выбранная клетка")
        self.instruction22 = Text(self.game, x=400, y=400, text="1.2 Нажми на красную клетку, чтобы отменить выбор")
        self.instruction23 = Text(self.game, x=300, y=435, text="1.3 Можешь выбрать белую клетку")
        self.instruction3 = Text(self.game, x=200, y=470, text="2 Зеленая - можно ходить")
        self.instruction4 = Text(self.game, x=300, y=505, text="3 Оранжевая - обмен войсками")
        self.instruction5 = Text(self.game, x=390, y=540, text="4 Прокруткой мыши добавляй/убавляй кол-во юнитов")
        self.objects = [self.map,self.instruction1, self.instruction2,self.instruction21,self.instruction22,
                        self.instruction23,self.instruction3, self.instruction4, self.instruction5]


    def set_main_scene(self):
        self.set_next_scene(self.game.MAIN_SCENE_INDEX)

    def set_map_scene(self):
        self.set_next_scene(self.game.MAP_SCENE_INDEX)

    def set_quest_scene(self):
        self.set_next_scene(self.game.QUESTS_SCENE_INDEX)

    def exit(self):
        self.game.game_over = True

