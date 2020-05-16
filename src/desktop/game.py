import sys

import pygame
from objects.sfx_player import SoundPlayer
from scenes.final import FinalScene
from scenes.main import MainScene
from scenes.menu import MenuScene
from scenes.map import MapScene
from scenes.quests import QuestScene
from scenes.login import LoginScene
from scenes.team import TeamScene


class Game:
    MENU_SCENE_INDEX = 0
    MAIN_SCENE_INDEX = 1
    GAMEOVER_SCENE_INDEX = 2
    QUESTS_SCENE_INDEX = 3
    MAP_SCENE_INDEX = 4
    LOGIN_SCENE_INDEX = 5
    TEAM_SCENE_INDEX = 6

    def __init__(self, width=800, height=600):
        pygame.mixer.init(22050, -16, 2, 64)
        self.sfx_player = SoundPlayer
        self.sfx_player.load()
        self.width = width
        self.height = height
        self.size = self.width, self.height
        self.create_window()
        self.game_over = False
        self.wall_collision_count = 0
        self.ticks = 0
        self.scenes = [MenuScene(self),
                       MainScene(self),
                       FinalScene(self), QuestScene(self), MapScene(self), LoginScene(self), TeamScene(self)]
        self.current_scene = 5
        self.team = None

    def create_window(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.size, pygame.RESIZABLE)

    def main_loop(self):

        while not self.game_over:
            eventlist = pygame.event.get()
            for event in eventlist:
                if event.type == pygame.QUIT:
                    print('Пользователь нажал крестик')
                    self.game_over = True

            self.scenes[self.current_scene].process_frame(eventlist)
        sys.exit(0)
