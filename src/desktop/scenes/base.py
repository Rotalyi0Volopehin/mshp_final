
import pygame

from constants import Color


class Scene:
    """Базовый класс сцен"""
    def __init__(self, game):
        """Получение главного класса, создание контейнера объектов на сцене"""
        self.game = game
        self.screen = self.game.screen
        self.objects = []
        self.create_objects()

    def create_objects(self):
        """Создание объектов сцены"""
        pass

    def process_frame(self, eventlist):
        """Компановка трех процессов"""
        self.process_all_events(eventlist)
        self.process_all_logic()
        self.process_all_draw()

    def process_all_events(self, eventlist):
        """Выполнение процесса событий всех объектов"""
        for event in eventlist:
            self.process_current_event(event)

    def process_current_event(self, event):
        """Выполнение процесса событий всех элементов в объекте"""
        for item in self.objects:
            item.process_event(event)
        self.additional_event_check(event)

    def additional_event_check(self, event):
        """Выполнение процесса событий всех элементов"""
        pass

    def process_all_logic(self):
        """Выполнение процесса логики всех элементов"""
        for item in self.objects:
            item.process_logic()
        self.additional_logic()

    def additional_logic(self):
        """Выполнение процесса событий всех элементов"""
        pass

    def process_all_draw(self):
        """Выполнение процесса отрисовки всех элементов"""
        self.screen.fill(Color.BLACK)
        for item in self.objects:
            item.process_draw()
        self.additional_draw()
        pygame.display.flip()  # double buffering

    def additional_draw(self):
        """Выполнение процесса отрисовки всех элементов"""
        pass

    # event
    def on_gone_to_deeper_scene_from_this(self):
        """При переходе на другую сцену, выполить"""
        pass

    # event
    def on_closed(self):
        """При закрытии"""
        pass

    # event
    def on_returned_to_this_scene(self):
        """При возвращении к данной сцене"""
        pass
