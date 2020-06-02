"""Описание класса"""
class DrawObject:
    """Базовый класс рисующихся объектов"""
    def __init__(self, game):
        """Инит основного класса игры"""
        self.game = game

    def process_event(self, event):
        """Базовая функция событий"""
        pass

    def process_logic(self):
        """Базовая функция логики"""
        pass

    def process_draw(self):
        """Базовая функция отрисовки"""
        pass