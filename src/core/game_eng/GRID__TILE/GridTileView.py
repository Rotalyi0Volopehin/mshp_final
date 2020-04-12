from objects.base import DrawObject


class GridTileView(DrawObject):
    def __init__(self, game, model, controller):
        super().__init__(game)
        print("view added")
        self.model = model
        self.controller = controller

    def process_draw(self):
        for row in range(self.model.height):
            for column in range(self.model.width):
                cell = self.model.getCell(row,column)
                if cell:
                    cell.process_draw()
