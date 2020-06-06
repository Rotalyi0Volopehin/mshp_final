from scenes.base import Scene
from objects.button import Btn


class MainMenuScene(Scene):
    def create_objects(self):
        waiting_room_button = Btn(self.game, (300, 255, 100, 40), text="Текущая сессия",
                                  function=self.__goto_waiting_room)
        quest_button = Btn(self.game, (400, 255, 100, 40), text="Квесты", function=self.__set_quest_scene)
        quit_account_button = Btn(self.game, (400, 305, 100, 40), text="из аккаунта",
                                  function=self.__quit_account)
        exit_button = Btn(self.game, (300, 305, 100, 40), text="Выход", function=self.game.exit)
        self.objects.extend([
            waiting_room_button,
            quest_button,
            quit_account_button,
            exit_button,
        ])

    def __quit_account(self):
        from scenes.login import LoginScene
        self.game.set_origin_scene(LoginScene)

    def __goto_waiting_room(self):
        from scenes.waiting_room import WaitingRoomScene
        self.game.goto_deeper_scene(WaitingRoomScene)

    def __set_quest_scene(self):
        from scenes.quests import QuestScene
        self.game.goto_deeper_scene(QuestScene)
