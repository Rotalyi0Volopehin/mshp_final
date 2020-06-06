from scenes.base import Scene
from objects.text import Text
from ws.parcel_manager import ParcelManager
from net_connection.request_ids import RequestID
from net_connection.response_ids import ResponseID
from game_eng.player_turn import PlayerTurn
from io_tools.binary_writer import BinaryWriter


class GSSyncScene(Scene):
    def __init__(self, game, post_changes_func, get_changes_func):
        super().__init__(game)
        self.post_changes_func = post_changes_func
        self.get_changes_func = get_changes_func
        if self.game.current_scene.game_vc.model.current_player.id == self.game.logged_user_id:
            self.__post_changes()
        else:
            self.__get_changes()

    def create_objects(self):
        self.objects.append(Text(self.game, text="Синхронизация ...", x=self.game.width >> 1, y=self.game.height >> 1))

    def __post_changes(self):
        stream = BinaryWriter()
        PlayerTurn.write(stream, self.game.current_scene.game_vc.model.player_action)
        ParcelManager.send_parcel([RequestID.POST_CHANGES, stream])
        ParcelManager.receive_parcel_async(self.__post_response_parcel_handler)

    def __get_changes(self):
        ParcelManager.send_parcel([RequestID.GET_CHANGES])
        ParcelManager.receive_parcel_async(self.__get_response_parcel_handler)

    def __post_response_parcel_handler(self, parcel):
        if parcel[0] == ResponseID.FAIL:
            from scenes.main_menu import MainMenuScene
            self.game.set_origin_scene(MainMenuScene)
        else:
            self.game.return_to_upper_scene()
            self.post_changes_func()

    def __get_response_parcel_handler(self, parcel):
        if parcel[0] == ResponseID.DATA:
            stream = parcel[1]
            player_turn = PlayerTurn.read(stream)
            self.get_changes_func(player_turn)
        self.game.return_to_upper_scene()
