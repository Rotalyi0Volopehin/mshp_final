import sys
import pygame
import time

from pygame.locals import *
from pygame_textinput import TextInput
from PIL import Image


class GIFImage(object):
    def __init__(self, filename, game):
        self.filename = filename
        self.image = Image.open(filename)
        self.frames = []
        self.get_frames()
        self.game = game
        self.screen = self.game.screen
        self.cur = 0
        self.ptime = time.time()

        self.running = True
        self.breakpoint = len(self.frames) - 1
        self.startpoint = 0
        self.reversed = False

    def process_logic(self):
        pass

    def process_draw(self):
        self.render(self.screen, (125,70))

    def process_event(self, event):
        pass

    def get_rect(self):
        print(self.image.size)
        return pygame.rect.Rect((0, 0), self.image.size)

    def get_frames(self):
        image = self.image

        pal = image.getpalette()
        base_palette = []
        for i in range(0, len(pal), 3):
            rgb = pal[i:i + 3]
            base_palette.append(rgb)

        all_tiles = []
        try:
            while 1:
                if not image.tile:
                    image.seek(0)
                if image.tile:
                    all_tiles.append(image.tile[0][3][0])
                image.seek(image.tell() + 1)
        except EOFError:
            image.seek(0)

        all_tiles = tuple(set(all_tiles))

        try:
            while 1:
                try:
                    duration = image.info["duration"]
                except:
                    duration = 100

                duration *= .001  # convert to milliseconds!
                cons = False

                x0, y0, x1, y1 = (0, 0) + image.size
                if image.tile:
                    tile = image.tile
                else:
                    image.seek(0)
                    tile = image.tile
                if len(tile) > 0:
                    x0, y0, x1, y1 = tile[0][1]

                if all_tiles:
                    if all_tiles in ((6,), (7,)):
                        cons = True
                        pal = image.getpalette()
                        palette = []
                        for i in range(0, len(pal), 3):
                            rgb = pal[i:i + 3]
                            palette.append(rgb)
                    elif all_tiles in ((7, 8), (8, 7)):
                        pal = image.getpalette()
                        palette = []
                        for i in range(0, len(pal), 3):
                            rgb = pal[i:i + 3]
                            palette.append(rgb)
                    else:
                        palette = base_palette
                else:
                    palette = base_palette

                pi = pygame.image.fromstring(image.tobytes(), image.size, image.mode)
                pi.set_palette(palette)
                if "transparency" in image.info:
                    pi.set_colorkey(image.info["transparency"])
                pi2 = pygame.Surface(image.size, SRCALPHA)
                if cons:
                    for i in self.frames:
                        pi2.blit(i[0], (0, 0))
                pi2.blit(pi, (x0, y0), (x0, y0, x1 - x0, y1 - y0))

                self.frames.append([pi2, duration])
                image.seek(image.tell() + 1)
        except EOFError:
            pass

    def render(self, screen, pos):
        if self.running:
            if time.time() - self.ptime > self.frames[self.cur][1]:
                if self.reversed:
                    self.cur -= 1
                    if self.cur < self.startpoint:
                        self.cur = self.breakpoint
                else:
                    self.cur += 1
                    if self.cur > self.breakpoint:
                        self.cur = self.startpoint
        screen.blit(self.frames[self.cur][0], pos)

    def seek(self, num):
        self.cur = num
        if self.cur < 0:
            self.cur = 0
        if self.cur >= len(self.frames):
            self.cur = len(self.frames) - 1

    def set_bounds(self, start, end):
        if start < 0:
            start = 0
        if start >= len(self.frames):
            start = len(self.frames) - 1
        if end < 0:
            end = 0
        if end >= len(self.frames):
            end = len(self.frames) - 1
        if end < start:
            end = start
        self.startpoint = start
        self.breakpoint = end

    def pause(self):
        self.running = False

    def play(self):
        self.running = True

    def rewind(self):
        self.seek(0)

    def fastforward(self):
        self.seek(self.length() - 1)

    def get_height(self):
        return self.image.size[1]

    def get_width(self):
        return self.image.size[0]

    def get_size(self):
        return self.image.size

    def length(self):
        return len(self.frames)

    def reverse(self):
        self.reversed = not self.reversed

    def reset(self):
        self.cur = 0
        self.ptime = time.time()
        self.reversed = False

    def copy(self):
        new = GIFImage(self.filename)
        new.running = self.running
        new.breakpoint = self.breakpoint
        new.startpoint = self.startpoint
        new.cur = self.cur
        new.ptime = self.ptime
        new.reversed = self.reversed
        return new


class Button:
    def __init__(self, x, y, text, image_press, image_unpress):

        self.size = [190, 45]  # Размер кнопки
        self.image_button = pygame.image.load(image_press)  # Загружаем изображение исходной кнопки
        self.text = text  # Текст кнопки
        self.x = x  # Позиция х кнопки
        self.y = y  # Позиция у кнопки
        self.clicked = False
        self.rect_button = pygame.Rect(self.x, self.y, self.size[0],
                                       self.size[1])  # Прямоугольник для создания коллизии с курсором
        self.rect_image_button = self.image_button.get_rect()
        """Создание кнопки при нажатии на нее"""
        self.image_click = pygame.image.load(image_press)
        self.image_put_on_button = pygame.image.load(image_unpress)

    def create_button(self):
        """Создает кнопку на экране"""
        font = pygame.font.Font(None, 36)
        text_button = font.render(self.text, True, (240, 240, 240))  # Создаем изображение с текстом
        text_rect = text_button.get_rect()  # Возвращаем прямоугольник который занимает текст
        text_rect.center = self.rect_image_button.center  # Делаем текст посередине кнопки
        self.image_button.blit(text_button, text_rect)
        self.image_click.blit(text_button, text_rect)
        self.image_put_on_button.blit(text_button, text_rect)

    def drawbutton(self, screen):
        if not(self.clicked):
            screen.blit(self.image_click,(self.x, self.y))
        else:
            screen.blit(self.image_put_on_button, (self.x, self.y))


from scenes.final import FinalScene
from scenes.main import MainScene
from scenes.menu import MenuScene
from scenes.map import MapScene
from scenes.quests import QuestScene
from scenes.login import LoginScene
from player import Player

class Game:
    MENU_SCENE_INDEX = 0
    MAIN_SCENE_INDEX = 1
    GAMEOVER_SCENE_INDEX = 2
    QUESTS_SCENE_INDEX = 3
    MAP_SCENE_INDEX = 4
    LOGIN_SCENE_INDEX = 5

    def __init__(self, width=800, height=600):
        self.width = width
        self.player = Player()
        self.height = height
        self.size = self.width, self.height
        self.game_over = False
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()


    def main_loop(self):
        pygame.init()
        pygame.display.set_caption("Войти/выйти")
        self.create_window()
        self.game_over = False
        self.wall_collision_count = 0
        self.ticks = 0
        self.scenes = [MenuScene(self), MainScene(self), FinalScene(self), QuestScene(self), MapScene(self), LoginScene(self)]
        self.current_scene = 5
        while not self.game_over:
            eventlist = pygame.event.get()
            for event in eventlist:
                if event.type == pygame.QUIT:
                    self.game_over = True
            if not self.game_over:
                self.scenes[self.current_scene].process_frame(eventlist)
                self.clock.tick(30)
        pygame.quit()
        sys.exit()

    def create_window(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.size, pygame.RESIZABLE)
