from scenes.base import Scene
from objects.text import Text
from ws.parcel_manager import ParcelManager
from net_connection.request_ids import RequestID
from game_eng.player_turn import PlayerTurn
from io_tools.binary_writer import BinaryWriter


class GSSyncScene(Scene):
    def create_objects(self):
        self.objects.append(Text(self.game, text="Синхронизация ...", x=self.game.width >> 1, y=self.game.height >> 1))
        if self.game.current_scene.game_vc.model.current_player.id == self.game.logged_user_id:
            self.__post_changes()
        else:
            self.__request_changes()

    def __post_changes(self):
        stream = BinaryWriter()
        PlayerTurn.write(stream, self.game.current_scene.game_vc.model.player_action)
        ParcelManager.send_parcel([RequestID.POST_CHANGES, stream])
        ParcelManager.receive_parcel_async(self.__post_response_parcel_handler)

    def __request_changes(self):
        ParcelManager.send_parcel([RequestID.GET_CHANGES])
        ParcelManager.receive_parcel_async(self.__get_response_parcel_handler)

    def __post_response_parcel_handler(self):
        pass

    def __get_response_parcel_handler(self):
        pass
