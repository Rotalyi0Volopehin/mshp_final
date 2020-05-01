import pygame
import request_parcel_helpers.user_logging as user_logging

from pygame.locals import *
from constants import Color
from scenes.base import Scene
from objects.text_input import Txtinput
from objects.button import Btn
from objects.text import Text
from objects.gifimage import GIFImage
from net_connection.response_ids import ResponseID
from ws.parcel_manager import ParcelManager
from ws.channel import Channel

from objects.gifimg import GIFImage

class LoginScene(Scene):
    def init_form(self):
        self.login = Txtinput(self.game, False, 170, 20)
        self.password = Txtinput(self.game, False, 180, 80)
        self.button_enter = Btn(self.game, (350, 350, 100, 40), Color.WHITE, "Войти", self.on_login_button_click)
        self.button_register = Btn(self.game, (350, 400, 100, 40), Color.WHITE, 'Регистрация', self.on_reg_button_click)
        self.trailer = GIFImage("backimage.gif", self.game)

        self.button_enter = Btn(self.game, (350, 350, 100, 40), Color.WHITE, "Войти", self.on_login_button_click)
        self.button_register = Btn(self.game, (350, 400, 100, 40), Color.WHITE, 'Регистрация', self.on_reg_button_click)
        self.text_login = Text(self.game, font_name='Comic Sans', font_size=36, is_bold=False,
                               is_italic=False, text='Логин:',
                               color=(255, 255, 100), x=125, y=30)
        self.text_reg = Text(self.game, font_name='Comic Sans', font_size=36, is_bold=False,
                             is_italic=False, text='Пароль:',
                             color=(255, 255, 100), x=125, y=90)

    def load_backimage(self):
        self.trailer = GIFImage("backimage.gif", self.game)

    def load_sound(self):
        pygame.mixer.music.load('soundtrack.wav')
        pygame.mixer.music.set_volume(0.5)

    def collect_objects(self):
        self.objects = [self.trailer, self.login, self.password,
                        self.button_enter, self.button_register,
                        self.text_login, self.text_reg, ]

    def create_objects(self):
        if not Channel.try_connect():  # TODO: заменить на сообщение с кнопкой для повторной попытки
            raise Exception("Cannot connect to server!")
        self.init_form()
        self.load_backimage()
        self.load_sound()
        self.collect_objects()
        pygame.mixer.music.play(-1)

    def set_menu_scene(self):
        self.set_next_scene(self.game.MENU_SCENE_INDEX)

    def on_login_button_click(self):
        login = self.login.internal_txtinput.get_text()
        password = self.password.internal_txtinput.get_text()
        user_logging.send_login_request(login, password)

        def handler_cloak(parcel):
            self.login_response_parcel_handler(parcel)
        ParcelManager.receive_parcel_async(handler_cloak)

    def login_response_parcel_handler(self, parcel):
        response_id = parcel[0]
        if response_id == ResponseID.ERROR:
            error_id = parcel[1]
            raise Exception("Server says that client is not right! ResponseError #" + str(error_id.value))
        if response_id == ResponseID.FAIL:
            pass  # TODO: реализовать вывод ошибки
        elif response_id == ResponseID.SUCCESS:
            self.set_menu_scene()

    def on_reg_button_click(self):
        pass  # TODO: сделать редирект в браузер на страницу регистрации
