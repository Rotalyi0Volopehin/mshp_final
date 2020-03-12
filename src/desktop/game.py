from pygame_textinput import TextInput
from PIL import Image
import pygame
from pygame.locals import *
import json
import time
import socket

class GIFImage(object):
    def __init__(self, filename):
        self.filename = filename
        self.image = Image.open(filename)
        self.frames = []
        self.get_frames()

        self.cur = 0
        self.ptime = time.time()

        self.running = True
        self.breakpoint = len(self.frames) - 1
        self.startpoint = 0
        self.reversed = False

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


class Game:

    def __init__(self, width=500, height=300):
        self.width = width
        self.height = height
        self.size = self.width, self.height
        self.game_over = False
        self.login = TextInput(antialias=False, cursor_color=(0, 255, 0))
        self.password = TextInput(antialias=False, cursor_color=(255, 112, 184))
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

        self.trailer = GIFImage("backimage.gif")


        self.enter = Button(200, 150, "Войти", "button_pressed.png", "button_not_pressed.png")
        self.enter.create_button()
        self.register = Button(167, 200, "Регистрация", "button_pressed_2.png", "button_not_pressed_2.png")
        self.register.create_button()

        self.font = pygame.font.Font(None, 36)
        self.textl = self.font.render("Логин", 1, (143, 254, 9))
        self.placel = self.textl.get_rect(center=(125, 30))

        self.font = pygame.font.Font(None, 36)
        self.textp = self.font.render("Пароль", 1, (9, 254, 243))
        self.placep = self.textp.get_rect(center=(125, 90))

    def main_loop(self):
        pygame.init()
        pygame.mixer.music.load('soundtrack.mp3')
        pygame.display.set_caption("Войти/выйти")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        while True:
            self.screen.fill((225, 225, 225))

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if event.pos[1] >= 50 and event.pos[1] <= 50 + self.login.font_size:
                            self.login.antialias = True
                            self.password.antialias = False
                        if event.pos[1] >= 100 and event.pos[1] <= 100 + self.password.font_size:
                            self.login.antialias = False
                            self.password.antialias = True

                    if self.enter.rect_button.collidepoint(event.pos[0],event.pos[1]):
                        self.enter.clicked = True
                        #TODO:
                        # DATA = {"data":
                        #            {"hostname":"localhost",
                        #             "ipaddress":"serverhost",
                        #             "login":login.get_text(),
                        #             "password":password.get_text()}}
                        # raw_data = json.dumps(DATA, ensure_ascii=False).encode("utf-8")
                        # socket = socket.socket()
                        # a.connect(('serverhost', 'port'))
                        # socket.send(raw_data)
                        # print((socket.recv(1000)).decode('utf-8'))
                        # Server responses us
                        # IF DATA.ISVALID == TRUE -> THEN GO PLAY CS GO
                    if self.register.rect_button.collidepoint(event.pos[0],event.pos[1]):
                        self.register.clicked = True
                        print('REGISTRACTION')

                if event.type == pygame.MOUSEBUTTONUP and self.enter.rect_button.collidepoint(event.pos[0],event.pos[1]):
                    self.enter.clicked = False
                if event.type == pygame.MOUSEBUTTONUP and self.register.rect_button.collidepoint(event.pos[0],event.pos[1]):
                    self.register.clicked = False




            if self.login.antialias:
                if self.login.update(events):
                    print(self.login.get_text())
            if self.password.antialias:
                if self.password.update(events):
                    print(self.password.get_text())
            # Blit its surface onto the screen
            self.trailer.render(self.screen, (0, 0))
            pygame.draw.rect(self.screen, [244, 255, 89], [100,50, 250,25], 0)
            self.screen.blit(self.login.get_surface(), (100, 50))
            pygame.draw.rect(self.screen, [244, 255, 89], [100, 103, 250, 25], 0)
            self.screen.blit(self.password.get_surface(), (100, 103))
            self.screen.blit(self.textl, self.placel)
            self.screen.blit(self.textp, self.placep)
            self.enter.drawbutton(self.screen)
            self.register.drawbutton(self.screen)
            pygame.display.update()
            self.clock.tick(30)
