from game_eng.GRID__TILE.grid_controller import GridTileController
from game_eng.GRID__TILE.grid_model import GridModel
from game_eng.GRID__TILE.grid_view import GridTileView
from scenes.base import Scene


class MenuScene(Scene):
    def create_objects(self):
        grid_model = GridModel(self.game)
        self.grid_controller = GridTileController(grid_model)
        grid_view = GridTileView(self.game, grid_model, self.grid_controller)
        self.grid_controller.init_view(grid_view)
        grid_view.process_draw()
        self.objects = [grid_view]

    def set_main_scene(self):
        self.set_next_scene(self.game.MAIN_SCENE_INDEX)

    def process_event(self,event):
        self.grid_controller.process_event(event)

    def exit(self):
        self.game.game_over = True
