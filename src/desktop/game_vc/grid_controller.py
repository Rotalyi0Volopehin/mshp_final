import pygame

from constants import Color


class GridTileController:
    def __init__(self, model):
        self.model = model
        self.ability = False

    def init_view(self, view):
        self.view = view

    def process_logic(self):
        pass

    def process_draw(self):
        pass

    def process_event(self, event):
        for ability in self.view.abilities:
            ability.process_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.on_click(event)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
            self.on_scroll(1)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
            self.on_scroll(-1)

    def on_click(self, event):
        clicked_cell = self.model.inPolygon(event.pos[0], event.pos[1])
        if clicked_cell is not None:
            if not self.ability:
                self.clicking_cell(clicked_cell)
            else:
                self.ability_execute(clicked_cell)

    def ability_execute(self,clicked_cell):
        if self.ability == "EMP":
            self.model.ability_emp(clicked_cell)
        elif self.ability == "FISH":
            self.model.ability_fishing(clicked_cell)
        self.ability = None

    def clicking_cell(self,clicked_cell):
        if clicked_cell.return_color() == Color.WHITE:
            self.model.set_all_team_color()
            self.model.set_cell_color_x_y(clicked_cell.x, clicked_cell.y, Color.RED)
            self.model.make_cells_green(clicked_cell)
        elif clicked_cell.return_color() == Color.RED:
            self.model.set_all_team_color()
        elif clicked_cell.return_color() == Color.GREEN:
            orange = self.model.get_cell_by_colour(Color.ORANGE)
            self.model.make_cell_green(orange)
            self.model.set_cell_color_x_y(clicked_cell.x, clicked_cell.y, Color.ORANGE)
        elif clicked_cell.return_color() == Color.ORANGE:
            self.model.make_cell_green(clicked_cell)

    def on_scroll(self, value):
        origin_cell = self.model.get_cell_by_colour(Color.RED)
        target_cell = self.model.get_cell_by_colour(Color.ORANGE)
        self.model.move_units(origin_cell, target_cell, value)

    def set_ability_emp(self):
        self.ability = "EMP"

    def set_ability_fishing(self):
        self.ability = "FISH"
