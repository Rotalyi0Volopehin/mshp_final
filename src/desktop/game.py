import pygame
import exceptions

from scenes.base import Scene
from scenes.login import LoginScene


class Game:
    @property
    def main_loop_duration(self) -> int:
        return 25

    def __init__(self, width=800, height=600):
        self.clock = pygame.time.Clock()
        self.__init_window(width, height)
        self.__init_scenes()

    def __init_window(self, width, height):
        self.width = width
        self.height = height
        self.size = self.width, self.height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Network Confrontation")
        self.screen = pygame.display.set_mode(self.size, pygame.RESIZABLE)

    def __init_scenes(self):
        self.scene_stack = []
        self.set_origin_scene(LoginScene)

    def set_origin_scene(self, new_scene_type: type, extra_kwargs: dict = None):
        if not issubclass(new_scene_type, Scene):
            raise exceptions.ArgumentTypeException()
        for scene in self.scene_stack:
            scene.on_closed()
        self.__current_scene = new_scene_type(self) if extra_kwargs is None else new_scene_type(self, **extra_kwargs)
        self.scene_stack = [self.__current_scene]

    def goto_deeper_scene(self, new_scene_type: type, extra_kwargs: dict = None):
        if not issubclass(new_scene_type, Scene):
            raise exceptions.ArgumentTypeException()
        prev_scene = self.__current_scene
        self.__current_scene = new_scene_type(self) if extra_kwargs is None else new_scene_type(self, **extra_kwargs)
        self.scene_stack.append(self.__current_scene)
        prev_scene.on_gone_to_deeper_scene_from_this()

    def return_to_upper_scene(self):
        self.scene_stack.pop().on_closed()
        self.__current_scene = self.scene_stack[-1]
        self.__current_scene.on_returned_to_this_scene()

    @property
    def current_scene(self):
        return self.__current_scene

    def main_loop(self):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    Game.exit()
            self.current_scene.process_frame(events)
            self.clock.tick(self.main_loop_duration)  # это не "sleep(dur)", а "sleep(dur - elapsed)"

    @staticmethod
    def exit():
        from ws.channel import Channel
        Channel.halt_loop()
        exit()
