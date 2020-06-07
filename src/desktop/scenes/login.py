import pygame
import os.path as path
import request_parcel_helpers.user_logging as user_logging
import webbrowser
import user_info

from constants import Color
from net_connection.response_ids import ResponseID
from objects.button import Btn
from objects.gifimage import GIFImage
from objects.text import Text, TextAlignment
from objects.text_input import TextInput
from objects.password_input import PasswordInput
from scenes.base import Scene
from ws.channel import Channel
from ws.parcel_manager import ParcelManager


class LoginScene(Scene):
    def init_form(self):
        self.login_textbox = TextInput(self.game, False, 230, 38, 11)
        self.password_textbox = PasswordInput(self.game, False, 230, 98, 18)
        button_register = Btn(self.game, (350, 400, 100, 40), Color.WHITE, 'Регистрация', self.on_reg_button_click)
        trailer = GIFImage(path.join("images", "login_backimage.gif"), self.game)
        login_label = Text(self.game, font_size=36, is_bold=False, is_italic=False,
                           text='Логин:', color=Color.YELLOW, x=225, y=30, alignment=TextAlignment.RIGHT)
        password_label = Text(self.game, font_size=36, is_bold=False, is_italic=False,
                              text='Пароль:', color=Color.YELLOW, x=225, y=90, alignment=TextAlignment.RIGHT)
        self.warning_label = Text(self.game, font_size=20, color=Color.RED,
                                  x=self.game.width >> 1, y=(self.game.height >> 1) + 20)
        self.objects.extend([
            trailer,
            self.login_textbox,
            self.password_textbox,
            button_register,
            login_label,
            password_label,
            self.warning_label,
        ])
        self.create_multiplayer_button()

    def create_multiplayer_button(self):
        if user_info.online:
            text = "Сетевая игра"
            color = Color.WHITE
        else:
            text = "Повторить попытку"
            color = Color.BLACK
        multiplayer_button = Btn(self.game, (325, 350, 150, 40), color, text, function=self.on_login_button_click)
        self.objects.append(multiplayer_button)

    def try_connect(self):
        user_info.online = Channel.try_connect()
        if user_info.online:
            self.objects.pop()
            self.create_multiplayer_button()
            self.warning_label.update_text("")
        else:
            self.warning_label.update_text("Нет соединения")

    def load_sound(self):
        pygame.mixer.music.load(path.join("sounds", "login_bgm.wav"))

    def create_objects(self):
        self.init_form()
        self.load_sound()
        pygame.mixer.music.play(-1)
        self.try_connect()

    def set_map_scene(self):
        from scenes.map import MapScene
        self.game.set_origin_scene(MapScene)

    def set_main_menu_scene(self):
        from scenes.main_menu import MainMenuScene
        self.game.set_origin_scene(MainMenuScene)

    def on_login_button_click(self):
        if user_info.online:
            login = self.login_textbox.internal_txtinput.get_text()
            password = self.password_textbox.internal_txtinput.get_text()
            user_logging.send_login_request(login, password)
            ParcelManager.receive_parcel_async(self.login_response_parcel_handler)
        else:
            self.try_connect()

    def on_enter_button_click(self):
        user_info.online = False
        self.set_map_scene()

    def login_response_parcel_handler(self, parcel):
        response_id = parcel[0]
        if response_id == ResponseID.FAIL:
            self.warning_label.update_text("Пользователя с указанными логином и паролем не существует")
        elif response_id == ResponseID.SUCCESS:
            user_info.user_id = parcel[1]
            self.set_main_menu_scene()

    @staticmethod
    def on_reg_button_click():
        webbrowser.open('http://network-conf.gq/registration/', new=1)

    def on_closed(self):
        pygame.mixer.music.stop()
