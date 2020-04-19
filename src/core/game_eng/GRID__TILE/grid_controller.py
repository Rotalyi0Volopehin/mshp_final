import pygame

from constants import Color


class GridTileController:
    def __init__(self, model):
        self.model = model

    def init_view(self,view):
        self.view = view

    def process_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.on_click(event)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
            self.on_scroll(1)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
            self.on_scroll(-1)

    def on_click(self, event):
        clicked_cell = self.model.inPolygon(event.pos[0], event.pos[1])
        if clicked_cell != None:
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

    def on_scroll(self,value):
        self.model.move_units(self.model.get_cell_by_colour(Color.RED), self.model.get_cell_by_colour(Color.ORANGE), value)
