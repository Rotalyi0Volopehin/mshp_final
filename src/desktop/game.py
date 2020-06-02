import sys

import exceptions
import pygame
from scenes.base import Scene
from scenes.login import LoginScene


class Game:
    '''Основной класс игры,
        отвечающий за создание окна(с его настройками),
        основной цикл игры и управляющий сценами
    '''
    @property
    def main_loop_duration(self) -> int:
        '''FPS'''
        return 25

    def __init__(self, width=800, height=600):
        """Установка ФПС, создание окна, инициализация сцен"""
        self.clock = pygame.time.Clock()
        self.scene_stack = []
        self.__current_scene = 0
        self.__init_window(width, height)
        self.__init_scenes()
        self.online = False

    def __init_window(self, width, height):
        """Создание окна с заданными шириной и высотой"""
        self.width = width
        self.height = height
        self.size = self.width, self.height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Network Confrontation")
        self.screen = pygame.display.set_mode(self.size, pygame.RESIZABLE)

    def __init_scenes(self):
        """Создание стека сцен, установка начальной сцены"""
        self.scene_stack = []
        self.set_origin_scene(LoginScene)

    def set_origin_scene(self, new_scene_type: type):
        """Установка начальной, заданной сцены"""
        if not issubclass(new_scene_type, Scene):
            raise exceptions.ArgumentTypeException()
        for scene in self.scene_stack:
            scene.on_closed()
        self.__current_scene = new_scene_type(self)
        self.scene_stack = [self.__current_scene]

    def goto_deeper_scene(self, new_scene_type: type):
        """Добавление в стек и установка данной сцены, как данная"""
        if not issubclass(new_scene_type, Scene):
            raise exceptions.ArgumentTypeException()
        prev_scene = self.__current_scene
        self.__current_scene = new_scene_type(self)
        self.scene_stack.append(self.__current_scene)
        prev_scene.on_gone_to_deeper_scene_from_this()

    def return_to_upper_scene(self):
        """Возвращение к предыдущей сцены в стеке"""
        self.scene_stack.pop().on_closed()
        self.__current_scene = self.scene_stack[-1]
        self.__current_scene.on_returned_to_this_scene()

    @property
    def current_scene(self):
        """Возвращение актуальной сцены"""
        return self.__current_scene

    def main_loop(self):
        """Основной цикл игры"""
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    Game.exit()
            self.current_scene.process_frame(events)
            self.clock.tick(self.main_loop_duration)

    @staticmethod
    def exit():
        """Функция выхода из игры"""
        pygame.quit()
        sys.exit()
