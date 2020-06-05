from objects.button import Btn
from scenes.base import Scene
from ws.parcel_manager import ParcelManager
from net_connection.request_ids import RequestID
from net_connection.response_ids import ResponseID
from objects.gs_info_plate import GSInfoPlate
from game_eng.game_model import GameModel


class MainMenuScene(Scene):
    def create_objects(self):
        exit_button = Btn(self.game, (350, 255, 100, 40), text="Выход", function=self.game.exit)
        self.objects.append(exit_button)
        self.gs_info_plate = GSInfoPlate(self.game, 400, 310, self.__set_gs_menu_scene, 120, self.__refresh)
        self.objects.append(self.gs_info_plate)

    def __set_gs_menu_scene(self, gs=None):
        if gs is None:
            self.__get_gs_from_server()
        else:
            from scenes.gs_menu import GSMenuScene
            self.game.goto_deeper_scene(GSMenuScene, {"gs": gs})

    def __refresh(self):
        parcel = [RequestID.GET_GS_INFO]
        ParcelManager.send_parcel(parcel)
        ParcelManager.receive_parcel_async(self.__refresh_response_receiver)

    def __refresh_response_receiver(self, parcel):
        response_id = parcel[0]
        if response_id == ResponseID.FAIL:
            pass  # TODO: реализовать вывод ошибки
        else:
            self.gs_info_plate.update_info_from_parcel(parcel)

    def __get_gs_from_server(self):
        ParcelManager.send_parcel([RequestID.GET_GAME_MODEL])
        ParcelManager.receive_parcel_async(self.__game_model_response_receiver)

    def __game_model_response_receiver(self, parcel):
        response_id = parcel[0]
        if response_id == ResponseID.FAIL:
            pass  # TODO: реализовать вывод ошибки
        else:
            gs = GameModel.read(parcel[1])
            self.__set_gs_menu_scene(gs)
