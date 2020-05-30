from .base import DrawObject
from net_connection.response_ids import ResponseID
from net_connection.participation_status_ids import ParticipationStatusID
from .text import Text
from .button import Btn


class GSInfoPlate(DrawObject):
    def __init__(self, game, pos_x, pos_y, play_button_func, auto_update_period=-1, auto_update_func=None):
        super().__init__(game)
        self.participation_status = ParticipationStatusID.NO_PARTICIPATION
        self.gs_title = None
        self.gathered_players_count = self.players_must_participate = None
        self.auto_update_period = auto_update_period
        self.auto_update_ticks_left = 0
        self.auto_update_func = auto_update_func
        self.participation_status_label = Text(game, is_bold=True, font_size=20, x=pos_x, y=pos_y)
        self.gs_title_label = Text(game, font_size=20, x=pos_x, y=pos_y + 20)
        self.player_count_label = Text(game, font_size=20, x=pos_x, y=pos_y + 40)
        self.update_labels()
        self.enter_gs_button = Btn(game, (pos_x - 50, pos_y + 30, 100, 40), text="Играть", function=play_button_func)

    def update_labels(self):
        if self.participation_status == ParticipationStatusID.NO_PARTICIPATION:
            participation_status = "Вы не участвуете в игровой сессии"
        elif self.participation_status == ParticipationStatusID.WAITING_FOR_BEGINNING:
            participation_status = "Набор игроков ..."
            self.gs_title_label = "Название сессии : " + self.gs_title
            self.player_count_label = f"Игроков набралось {self.gathered_players_count}/{self.players_must_participate}"
        else:
            participation_status = "Игра уже началась"
        self.participation_status_label.update_text(participation_status)

    def update_info_from_parcel(self, parcel: list):
        if parcel[0] == ResponseID.FAIL:
            raise Exception("Fail - error 400!")
        self.participation_status = parcel[1]
        if len(parcel) > 2:
            if self.participation_status != ParticipationStatusID.NO_PARTICIPATION:
                self.gs_title = parcel[2]
                self.gathered_players_count = parcel[3]
                self.players_must_participate = parcel[4]

    def process_logic(self):
        if self.auto_update_period >= 0:
            if self.auto_update_ticks_left == 0:
                self.auto_update_ticks_left = self.auto_update_period
                self.auto_update_func()
            self.auto_update_ticks_left -= 1

    def process_draw(self):
        self.participation_status_label.process_draw()
        if self.participation_status == ParticipationStatusID.WAITING_FOR_BEGINNING:
            self.gs_title_label.process_draw()
            self.player_count_label.process_draw()
        elif self.participation_status == ParticipationStatusID.PLAYING_GAME:
            self.enter_gs_button.process_draw()
