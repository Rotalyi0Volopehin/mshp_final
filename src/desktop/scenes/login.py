import pygame
import os.path as path
import request_parcel_helpers.user_logging as user_logging
import webbrowser
import user_info

from constants import Color
from net_connection.response_ids import ResponseID
from objects.button import Btn
from objects.gifimage import GIFImage
from objects.text import Text
from objects.text_input import TextInput
from objects.password_input import PasswordInput
from scenes.base import Scene
from ws.channel import Channel
from ws.parcel_manager import ParcelManager


class LoginScene(Scene):
    def init_form(self):
        self.login_textbox = TextInput(self.game, False, 170, 20, 11)
        self.password_textbox = PasswordInput(self.game, False, 180, 80, 18)
        button_enter = Btn(self.game, (350, 300, 100, 40), Color.WHITE, "Войти", self.on_enter_button_click)
        button_quest = Btn(self.game, (350, 500, 100, 40), Color.WHITE, "Квесты", self.on_quests_button_click)
        button_register = Btn(self.game, (350, 400, 100, 40), Color.WHITE, 'Регистрация', self.on_reg_button_click)
        trailer = GIFImage(path.join("images", "login_backimage.gif"), self.game)
        login_label = Text(self.game, font_name='Comic Sans', font_size=36, is_bold=False, is_italic=False,
                           text='Логин : ', color=Color.YELLOW, x=125, y=30)
        password_label = Text(self.game, font_name='Comic Sans', font_size=36, is_bold=False, is_italic=False,
                              text='Пароль : ', color=Color.YELLOW, x=125, y=90)
        multiplayer_enter_color = Color.WHITE if user_info.online else Color.BLACK
        button_multiplayer_enter = Btn(self.game, (350, 350, 100, 40), multiplayer_enter_color, "Сетевая игра",
                                       self.on_login_button_click if user_info.online else None)
        self.objects.extend([
            trailer,
            self.login_textbox,
            self.password_textbox,
            button_enter,
            button_multiplayer_enter,
            button_register,
            button_quest,
            login_label,
            password_label,
        ])

    def load_sound(self):
        pygame.mixer.music.load(path.join("sounds", "login_bgm.wav"))

    def create_objects(self):
        user_info.online = Channel.try_connect()  # TODO: заменить на сообщение с кнопкой для повторной попытки
        self.init_form()
        self.load_sound()
        pygame.mixer.music.play(-1)

    def set_quests_scene(self):
        path_1 = path.join("quests", "stats")
        file = open(path_1, 'r')
        if file.read() == '':
            from scenes.language_selection import LanguageScene
            file.close()
            self.game.set_origin_scene(LanguageScene)
        else:
            from scenes.quest import QuestScene
            file.close()
            self.game.set_origin_scene(QuestScene)

    def set_map_scene(self):
        from scenes.map import MapScene
        self.game.set_origin_scene(MapScene)

    def set_main_menu_scene(self):
        from scenes.main_menu import MainMenuScene
        self.game.set_origin_scene(MainMenuScene)

    def on_login_button_click(self):
        login = self.login_textbox.internal_txtinput.get_text()
        password = self.password_textbox.internal_txtinput.get_text()
        user_logging.send_login_request(login, password)
        ParcelManager.receive_parcel_async(self.login_response_parcel_handler)

    def on_enter_button_click(self):
        user_info.online = False
        self.set_map_scene()

    def on_quests_button_click(self):
        self.set_quests_scene()

    def login_response_parcel_handler(self, parcel):
        response_id = parcel[0]
        if response_id == ResponseID.FAIL:
            pass  # TODO: реализовать вывод ошибки
        elif response_id == ResponseID.SUCCESS:
            user_info.user_id = parcel[1]
            self.set_main_menu_scene()

    @staticmethod
    def on_reg_button_click():
        webbrowser.open('http://network-conf.gq/registration/', new=1)

    def on_closed(self):
        pygame.mixer.music.stop()
