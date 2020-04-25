from pygame_textinput import TextInput
from PIL import Image
import pygame
from pygame.locals import *
import json
import time
from constants import Color
from scenes.base import Scene
import socket
from objects.text_input import Txtinput
from objects.button import Btn
from objects.text import Text
from objects.gifimg import GIFImage
from objects.image import Image as Img

class LoginScene(Scene):
    def create_objects(self):
        self.login = Txtinput(self.game, False, 170, 20)
        self.image_bg = Img(self.game, file_name='images/Background.png', x=0, y=0)
        self.password = Txtinput(self.game, False, 180, 80)
        #self.trailer = GIFImage("backimage.gif", self.game)

        self.button_enter = Btn(self.game, (350, 350, 100, 40), Color.WHITE, "Войти", self.lg_on_click)
        self.button_register = Btn(self.game, (350, 400, 100, 40), Color.WHITE, 'Регистрация', self.rg_on_click)
        self.text_login = Text(self.game, font_name='Comic Sans', font_size=36, is_bold=False,
                               is_italic=False, text='Логин:',
                               color=(255, 255, 100), x=125, y=30)
        self.text_reg = Text(self.game, font_name='Comic Sans', font_size=36, is_bold=False,
                             is_italic=False, text='Пароль:',
                             color=(255, 255, 100), x=125, y=90)

        self.objects = [
                   # self.trailer,
                    self.image_bg,
                    self.password,
                    self.button_enter, self.button_register,
                    self.text_login, self.text_reg,
                    self.login
                        ]

    def set_menu_scene(self):
        self.set_next_scene(self.game.MENU_SCENE_INDEX)

    def lg_on_click(self):
        pass
        # тODO проверка сервера...
        # TODO:
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
        # IF DATA.ISVALID == TRUE -> THEN GO PLAY CS:GO

        self.set_menu_scene()  # если авторизировался выполнить

    def rg_on_click(self):
        pass
        # ODO зарегистрировать на сервере...
        # TODO:
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
        # IF DATA.ISVALID == TRUE -> THEN GO PLAY CS:GO
