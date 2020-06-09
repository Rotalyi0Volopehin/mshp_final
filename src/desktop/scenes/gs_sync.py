import user_info

from datetime import datetime
from scenes.base import Scene
from objects.text import Text
from ws.parcel_manager import ParcelManager
from net_connection.request_ids import RequestID
from net_connection.response_ids import ResponseID
from game_eng.player_turn import PlayerTurn
from io_tools.binary_writer import BinaryWriter


class GSSyncScene(Scene):
    def __init__(self, game, game_model, post_changes_func, get_changes_func, defeated_func):
        super().__init__(game)
        self.game_model = game_model
        self.post_changes_func = post_changes_func
        self.get_changes_func = get_changes_func
        self.defeated_func = defeated_func
        if (game_model.current_player.id == user_info.user_id) and (len(game_model.current_player_turn.actions) > 0):
            self.__get_delay_start = None
            self.__post_changes()
        else:
            self.__get_delay_start = datetime.utcnow().timestamp()

    def process_all_logic(self):
        super().process_all_logic()
        if (self.__get_delay_start is not None) and (datetime.utcnow().timestamp() - self.__get_delay_start > 1.0):
            self.__get_delay_start = None
            self.__get_changes()

    def create_objects(self):
        self.objects.append(Text(self.game, text="Синхронизация ...", x=self.game.width >> 1, y=self.game.height >> 1))

    def __post_changes(self):
        stream = BinaryWriter()
        PlayerTurn.write(stream, self.game_model.current_player_turn)
        ParcelManager.send_parcel([RequestID.POST_CHANGES, stream])
        ParcelManager.receive_parcel_async(self.__post_response_parcel_handler)

    def __get_changes(self):
        ParcelManager.send_parcel([RequestID.GET_CHANGES])
        ParcelManager.receive_parcel_async(self.__get_response_parcel_handler)

    def __post_response_parcel_handler(self, parcel):
        if parcel[0] == ResponseID.FAIL:
            from scenes.main_menu import MainMenuScene
            self.game.set_origin_scene(MainMenuScene)
            return
        self.game.return_to_upper_scene()
        self.post_changes_func()

    def __get_response_parcel_handler(self, parcel):
        if parcel[0] == ResponseID.FAIL:
            from scenes.main_menu import MainMenuScene
            self.game.set_origin_scene(MainMenuScene)
        elif parcel[0] == ResponseID.DEFEATED:
            self.defeated_func()
        elif parcel[0] == ResponseID.DATA:
            stream = parcel[1]
            self.game.return_to_upper_scene()
            self.get_changes_func(stream)
