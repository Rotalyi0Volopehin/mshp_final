import sys
import pygame

from objects.yandex_translate import Translator
from scenes.final import FinalScene
from scenes.main import MainScene
from scenes.menu import MenuScene
from scenes.map import MapScene
from scenes.quests_menu import QuestMenuScene
from scenes.login import LoginScene
from scenes.quest import QuestScene
from scenes.stats import StatsMenuScene
from scenes.fraction import FractionScene
from scenes.contacts.call_contact import CallContactScene
from scenes.contacts.pod_contact import PodContactScene
from scenes.contacts.cyb_contact import CybContactScene


class Game:
    MENU_SCENE_INDEX = 0
    GAMEOVER_SCENE_INDEX = 1
    QUEST_SCENE_INDEX = 2
    MAP_SCENE_INDEX = 3
    LOGIN_SCENE_INDEX = 4
    QUEST_MENU_SCENE_INDEX = 5
    STATS_SCENE_INDEX = 6
    CALL_CONTACT_SCENE_INDEX = 7
    POD_CONTACT_SCENE_INDEX = 8
    CYB_CONTACT_SCENE_INDEX = 9
    FRACTION_SCENE_INDEX = 10

    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.size = self.width, self.height
        self.create_window()
        self.game_over = False
        self.wall_collision_count = 0
        self.ticks = 0
        self.scenes = [MenuScene(self), FinalScene(self), QuestScene(self),
                       MapScene(self), LoginScene(self), QuestMenuScene(self), StatsMenuScene(self),
                       CallContactScene(self), PodContactScene(self), CybContactScene(self),
                       FractionScene(self)]

        self.current_scene = 0
        self.language = "en"
        self.translator = Translator()

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
