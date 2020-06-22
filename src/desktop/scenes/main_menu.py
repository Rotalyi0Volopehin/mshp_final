from scenes.base import Scene
from objects.button import Btn
from objects.text import Text
from os import path
from ws.parcel_manager import ParcelManager
from request_parcel_helpers.user_logging import send_logout_request
from net_connection.response_ids import ResponseID


class MainMenuScene(Scene):
    def create_objects(self):
        waiting_room_button = Btn(self.game, (300, 255, 100, 40), text="Текущая сессия",
                                  function=self.__goto_waiting_room)
        quest_button = Btn(self.game, (400, 255, 100, 40), text="Квесты", function=self.__set_quests_scene)
        quit_account_button = Btn(self.game, (400, 305, 100, 40), text="из аккаунта",
                                  function=self.__quit_account)
        exit_button = Btn(self.game, (300, 305, 100, 40), text="Назад", function=self.game.return_to_upper_scene)
        title = Text(self.game, font_size=72, text="NetWars", x=self.game.width >> 1, y=200)
        self.objects.extend([
            waiting_room_button,
            quest_button,
            quit_account_button,
            exit_button,
            title,
        ])

    def __quit_account(self):
        def logout_handler(parcel):
            if parcel[0] == ResponseID.SUCCESS:
                from scenes.login import LoginScene
                self.game.set_origin_scene(LoginScene)
        send_logout_request()
        ParcelManager.receive_parcel_async(logout_handler)

    def __goto_waiting_room(self):
        from scenes.waiting_room import WaitingRoomScene
        self.game.goto_deeper_scene(WaitingRoomScene)

    def __set_quests_scene(self):
        path_1 = path.join("quests", "stats")
        file = open(path_1, 'r')
        from scenes.language_selection import LanguageScene
        file.close()
        self.game.goto_deeper_scene(LanguageScene)
