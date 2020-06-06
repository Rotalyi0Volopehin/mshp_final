from objects.button import Btn
from scenes.base import Scene
from ws.parcel_manager import ParcelManager
from net_connection.request_ids import RequestID
from net_connection.response_ids import ResponseID
from objects.gs_info_plate import GSInfoPlate
from game_eng.game_model import GameModel


class WaitingRoomScene(Scene):
    def create_objects(self):
        back_button = Btn(self.game, (350, 255, 100, 40), text="Назад", function=self.game.return_to_upper_scene)
        self.objects.append(back_button)
        self.gs_info_plate = GSInfoPlate(self.game, 400, 310, self.__set_map_scene, self.__get_gs_from_server,
                                         120, self.__refresh)
        self.objects.append(self.gs_info_plate)

    def __set_map_scene(self):
        from scenes.map import MapScene
        self.game.return_to_upper_scene()
        self.game.goto_deeper_scene(MapScene, {"gs": self.gs})

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
            self.gs = GameModel.read(parcel[1])
            b = self.gs.turn_beginning_time
            self.gs_info_plate.set_waiting_for_first_turn_state(b)
