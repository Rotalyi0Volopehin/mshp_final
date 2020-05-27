from objects.button import Btn
from scenes.base import Scene
from game_vc.game_vc import GameVC
from ws.parcel_manager import ParcelManager
from net_connection.request_ids import RequestID
from net_connection.response_ids import ResponseID
from net_connection.participation_status_ids import ParticipationStatusID


class MainMenuScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.participation_status = ParticipationStatusID.NO_PARTICIPATION
        self.__refresh()

    def create_objects(self):
        exit_button = Btn(self.game, (350, 305, 100, 40), text="Выход", function=self.game.exit)
        self.objects.append(exit_button)
        # TODO: сделать, чтоб красиво '↻'
        refresh_button = Btn(self.game, (350, 255, 100, 40), text="Обновить данные", function=self.__refresh)
        self.objects.append(refresh_button)
        self.gs_button = Btn(self.game, (350, 205, 100, 40), text="Игровая сессия", function=self.__set_gs_menu_scene)

    def process_all_draw(self):
        visible = self.participation_status == ParticipationStatusID.PLAYING_GAME
        if visible:
            self.objects.append(self.gs_button)
        super().process_all_draw()
        if visible:
            self.objects.pop()

    def __set_gs_menu_scene(self):
        from scenes.gs_menu import GSMenuScene
        self.game.goto_deeper_scene(GSMenuScene)

    def __refresh(self):
        parcel = [RequestID.GET_PARTICIPATION_STATUS]
        ParcelManager.send_parcel(parcel)
        ParcelManager.receive_parcel_async(self.__refresh_response_receiver)

    def __refresh_response_receiver(self, parcel):
        response_id = parcel[0]
        if response_id == ResponseID.FAIL:
            pass  # TODO: реализовать вывод ошибки
        else:
            self.participation_status = parcel[1]
